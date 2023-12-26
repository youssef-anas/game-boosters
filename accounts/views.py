from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from accounts.forms import Registeration, ProfileEditForm, ProfileEditForm, PasswordEditForm
from django.contrib import messages
from django.shortcuts import render, redirect , HttpResponse, get_object_or_404
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseBadRequest, HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils import timezone
from django.contrib.auth.views import LoginView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login , logout
from wildRift.models import WildRiftDivisionOrder
from django.http import JsonResponse
from accounts.order_creator import  create_order
User = get_user_model()
from booster.models import Booster
from accounts.models import BaseOrder, Room, Message
from accounts.models import BaseUser

@csrf_exempt
def send_activation_email(user, request):
    # Generate a token for the user
    token = default_token_generator.make_token(user)

    # Build the activation URL
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_url = reverse('account.activate', kwargs={'uidb64': uid, 'token': token})
    activation_url = request.build_absolute_uri(activation_url)

    # Create the subject and message for the email
    subject = 'Activate Your Account'
    message = render_to_string('accounts/activation_email.html', {
        'user': user,
        'activation_url': activation_url,
    })

    # Send the email
    send_mail(subject, message, 'your@example.com', [user.email])

def create_chat_with_booster(customer,booster,orderId):
    isRoomExist = Room.get_specific_room(customer,orderId)
    if not isRoomExist:
        return Room.create_room_with_booster(customer,booster,orderId)
    else:
        return isRoomExist
    
def create_chat_with_admins(customer,orderId):
    isRoomExist = Room.get_specific_admins_room(customer,orderId)
    if not isRoomExist:
        return Room.create_room_with_admins(customer,orderId)
    else:
        return isRoomExist

@csrf_exempt
def register_view(request):
    invoice = request.session.get('invoice')
    payer_id = request.GET.get('PayerID')
    
    if invoice:
        if request.user.is_authenticated:
            order = create_order(invoice, payer_id, request.user)
            create_chat_with_admins(customer=request.user,orderId = order.order.id)
            create_chat_with_booster(customer=request.user,booster=None,orderId = order.order.id)
            return redirect(reverse_lazy('accounts.customer_side'))
        if request.method == 'POST':
            form = Registeration(request.POST,request.FILES)
            if form.is_valid():
                user = form.save()
                order = create_order(invoice, payer_id, user)
                login(request, user)
                # Send activation email
                # send_activation_email(user, request)
                # return render(request, 'accounts/activation_sent.html')
                create_chat_with_admins(customer=request.user, orderId = order.order.id)
                create_chat_with_booster(customer=request.user,booster=None,orderId = order.order.id)
                return redirect(reverse_lazy('accounts.customer_side'))
        form = Registeration()
        return render(request, 'accounts/register.html', {'form': form})
    
    
@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

@csrf_exempt
def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.email_verified_at = timezone.now()
        user.save()
        return render(request, 'accounts/.html')
    
    return HttpResponseBadRequest('Activation Link is Invalid or Has Expired.')

@csrf_exempt
def login_view(request):
    template_name = 'accounts/login.html'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("username", username)
        print("password", password)

        # Perform authentication
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            context = {'error_message': ''}
            return redirect(reverse_lazy('homepage.index'))
        else:
            # Authentication failed, handle it as needed
            context = {'error_message': 'Invalid Credentials'}
            return render(request, template_name, context)
    return render(request, template_name)
    
def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('homepage.index'))



def choose_booster(request):
    if request.method == 'POST':
        chosen_booster_id = request.POST.get('chosen_booster_id')
        order_id = request.POST.get('order_id')
        request.POST.get('admins_chat_slug')

        if chosen_booster_id and order_id:
            order = get_object_or_404(BaseOrder, pk=order_id)
            booster = get_object_or_404(BaseUser, id=chosen_booster_id)
            order.booster = booster
            order.save()
            create_chat_with_booster(request.user,booster,order_id)
            return redirect(reverse_lazy('accounts.customer_side'))
    return JsonResponse({'success': False})

def set_customer_data(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        customer_gamename = request.POST.get('gamename')
        customer_server = request.POST.get('server')
        customer_password = request.POST.get('password')
        booster = request.POST.get('chosen_booster_id')
        request.POST.get('admins_chat_slug')
        if customer_gamename and order_id and customer_server:
            order = get_object_or_404(BaseOrder, pk=order_id)
            order.customer_gamename = customer_gamename
            order.customer_server = customer_server 
            if customer_password :
                order.customer_password = customer_password
            order.save()
            if booster:
                create_chat_with_booster(User,booster,order_id)
                return redirect(reverse_lazy('accounts.customer_side'))
            return redirect(reverse_lazy('accounts.customer_side'))
    return JsonResponse({'success': False})

def tip_booster(request):
    if request.method == 'POST':
        tip = request.POST.get('tip')
        order_id = request.POST.get('order_id')
        booster = request.POST.get('booster')
        if tip and order_id and booster:
            room = Room.get_specific_room(request.user, order_id)
            msg = f'{request.user.first_name} tips {booster} with {tip}$'
            Message.create_tip_message(request.user,msg,room)
            return redirect(reverse_lazy('accounts.customer_side'))
        return JsonResponse({'success': False})

def customer_side(request):
    customer = BaseUser.objects.get(id = request.user.id)
    order = BaseOrder.objects.filter(customer=customer).last()
    id = order.id
    admins_chat_slug = f'roomFor-{request.user.username}-admins-{order.name}'
    # Chat with admins
    admins_room = Room.objects.get(slug=admins_chat_slug)
    admins_messages=Message.objects.filter(room=Room.objects.get(slug=admins_chat_slug)) 
    order = WildRiftDivisionOrder.objects.get(order__id=id)
    if order.order.is_done:
        return redirect(reverse_lazy('rate.page', kwargs={'order_id': order.order.id}))
    boosters = Booster.objects.filter(can_choose_me=True)
    # Chat with booster
    slug = request.GET.get('booster_slug') or None
    if not slug:
        specific_room = Room.get_specific_room(request.user, order.order.id)
        slug = specific_room.slug if specific_room else None
    if slug:
        room = Room.objects.get(slug=slug)
        messages=Message.objects.filter(room=Room.objects.get(slug=slug)) 
        context = {
            'user':User,
            "slug":slug,
            'messages':messages,
            'room':room,
            'boosters':boosters,
            'order':order,
            'admins_room':admins_room,
            'admins_room_name':admins_room,
            'admins_messages':admins_messages,
            'admins_chat_slug':admins_chat_slug
        }    
    else:
        context = {
            'user':User,
            "slug":None,
            'messages':None,
            'room':None,
            'boosters':boosters,
            'order':order,
            'admins_room':admins_room,
            'admins_room_name':admins_room,
            'admins_messages':admins_messages,
            'admins_chat_slug':admins_chat_slug
        } 
    template_name = 'accounts/customer_side.html'
    return render(request, template_name, context)

@login_required
def edit_customer_profile(request):
    profile_form = ProfileEditForm(instance=request.user)
    password_form = PasswordEditForm(user=request.user)

    if request.method == 'POST':
        if 'profile_submit' in request.POST:
            profile_form = ProfileEditForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profile Updated Successfully.')
                return redirect('edit.customer.profile')

        elif 'password_submit' in request.POST:
            password_form = PasswordEditForm(request.user, request.POST)
            if password_form.is_valid():
                password_form.save()
                messages.success(request, 'Password Changed Successfully.')
                return redirect('edit.customer.profile')

    return render(request, 'accounts/edit_profile.html', {'profile_form': profile_form, 'password_form': password_form})
