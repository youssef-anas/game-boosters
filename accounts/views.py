from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from accounts.controller.forms import Registeration, ProfileEditForm, ProfileEditForm, PasswordEditForm
from django.contrib import messages as NotifyMessage
from django.shortcuts import render, redirect , HttpResponse, get_object_or_404
from django.contrib.auth import get_user_model
from django.http import HttpResponseBadRequest, HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login , logout
from django.http import JsonResponse
from accounts.controller.order_creator import create_order
from accounts.controller.utils import refresh_order_page
User = get_user_model()
from accounts.models import BaseUser, BaseOrder, TokenForPay, Transaction, Tip_data
from chat.models import Room, Message
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
import secrets
from channels.db import database_sync_to_async
from accounts.controller.utils import get_boosters
from django_q.tasks import async_task
from .controller.tasks import update_database_task
from django.contrib import messages as messageForPageResponse
from accounts.models import PromoCode
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.controller.serializers import PromoCodeSerializer
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import random
from datetime import timedelta



def generate_random_5_digit_number():
    return random.randint(10000, 99999)


def send_activation_code(user) -> int:
    subject = 'Activate Your Account'
    users_list = [user.email]
    secret_key = generate_random_5_digit_number()

    html_content = render_to_string('chat/activation_email.html', {'secret_key': secret_key, 'user':user})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, 'madboost.customer@gmail.com', users_list)
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)

    user.activation_code = secret_key
    user.activation_time = timezone.now()
    user.save()
    return secret_key

def create_account(request):
    email = request.session.get('email')
    if email:
        user = get_object_or_404(BaseUser, email = email)
        send_activation_code(user)
        return redirect('accounts.activate.sent')
    if request.method == 'POST':
        form = Registeration(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_activation_code(user)
            request.session['email'] = user.email
            return redirect('accounts.activate.sent')
        else:
            return render(request, 'accounts/register.html', {'form': form})
    form =  Registeration()
    return render(request, 'accounts/register.html', {'form': form})


def activate_account_sent(request):
    email = request.session.get('email')
    return render(request, 'accounts/activation_sent.html', context={'email':email})


def activate_account(request, code):
    user = BaseUser.objects.get(activation_code=code)

    if not user:
        messageForPageResponse.error(request, 'Error in code')
        return redirect(reverse('accounts.activate.sent'))

    time_difference = timezone.now() - user.activation_time
    if time_difference > timedelta(minutes=1):
        return HttpResponseBadRequest("Activation time hasn't elapsed yet")

    user.is_active = True
    user.save()

    # Set the backend attribute on the user
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)

    messageForPageResponse.success(request, 'Your account has been activated successfully')
    return redirect(reverse('homepage.index'))

# from allauth.socialaccount.providers.openid.views import OpenIDLoginView

# class Custom_login(OpenIDLoginView):
#     template_name = "accounts/test.html"



def register_view(request):
    invoice = request.session.get('invoice')
    payer_id = request.GET.get('PayerID')
        # if request.method == 'POST':
        #     form = Registeration(request.POST,request.FILES)
        #     if form.is_valid():
        #         user = form.save()
        #         order = create_order(invoice, payer_id, user)
        #         login(request, user)
        #         # Send activation email
        #         # send_activation_email(user, request)
        #         # return render(request, 'accounts/activation_sent.html')
        #         Room.create_room_with_admins(request.user, order.order.name)
        #         Room.create_room_with_booster(request.user,booster, order.order.name)
        #         refresh_order_page()
        #         async_task(update_database_task,order.order.id)
        #         return redirect(reverse('accounts.customer_side', kwargs={'order_name': order.order.name}))
    if invoice:
        invoice_values = invoice.split('-')
        booster_id = int(invoice_values[12])
        try:
            booster = BaseUser.objects.get(id=booster_id, is_booster =True)
        except BaseUser.DoesNotExist:
            booster = None
        if request.user.is_authenticated:
            order = create_order(invoice, payer_id, request.user)
            Room.create_room_with_admins(request.user, order.order.name)
            Room.create_room_with_booster(request.user, booster, order.order.name)
            refresh_order_page()
            async_task(update_database_task,order.order.id)
            return redirect(reverse('accounts.customer_side', kwargs={'order_name': order.order.name}))
        else:
            form =  Registeration()
            return render(request, 'accounts/register.html', {'form': form})
    return HttpResponse("error in invoice")
    
    
@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')


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
        # TODO make it in kwrgs better than POST data
        chosen_booster_id = request.POST.get('chosen_booster_id')
        order_id = request.POST.get('order_id')

        if chosen_booster_id and order_id:
            order = get_object_or_404(BaseOrder, pk=order_id)
            booster = get_object_or_404(BaseUser, id=chosen_booster_id)
            order.booster = booster
            order.save()
            # Room.create_room_with_booster(request.user,booster,order.name)
            return redirect(reverse_lazy('accounts.customer_side'))
    return JsonResponse({'success': False})

def set_customer_data(request):
    if request.method == 'POST':
        # TODO use serializer better to validate data
        order_id = request.POST.get('order_id')
        customer_gamename = request.POST.get('gamename')
        customer_password = request.POST.get('password')
        booster = request.POST.get('chosen_booster_id')
        request.POST.get('admins_chat_slug')
        if customer_gamename and order_id:
            order = get_object_or_404(BaseOrder, pk=order_id)
            order.customer_gamename = customer_gamename
            if customer_password :
                order.customer_password = customer_password
            order.save()
            if booster:
                Room.create_room_with_booster(User,booster,order.name)
                return redirect(reverse_lazy('accounts.customer_side'))
            return redirect(reverse_lazy('accounts.customer_side'))
    return JsonResponse({'success': False})

@csrf_exempt
def tip_booster(request):
    if request.method == 'POST':
        tip = request.POST.get('tip')
        order_id = request.POST.get('order_id')
        booster = request.POST.get('booster')
        user = str(request.user.username)
        time = str(timezone.now())
        token = secrets.token_hex(14)
        token_with_data = '-'.join([user, tip, order_id, booster, token])
        token_for_pay, created = TokenForPay.objects.get_or_create(user=request.user, defaults={'token': token_with_data})
        
        if not created:
            token_for_pay.token = token_with_data
            token_for_pay.save()
    
        if tip and order_id and booster:
            invoice = f'tip-{user}-{tip}-{order_id}-{booster}-{time}'
            request.session['invoice'] = invoice
            paypal_dict = {
                "business": settings.PAYPAL_EMAIL,
                "amount": tip,
                "item_name": f"tip {booster}",
                "invoice": invoice,
                "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
                "return": request.build_absolute_uri(f"/accounts/tip_booster/success/{token_with_data}/"),
                "cancel_return": request.build_absolute_uri(f"/accounts/tip_booster/cancel/{token_with_data}/"),
            }
            # Create the instance.
            form = PayPalPaymentsForm(initial=paypal_dict)
            context = {"form": form}
            return render(request, "accounts/paypal.html", context,status=200)
        return JsonResponse({'success': False})
    
def success_tip(request,token):
    token_with_data = TokenForPay.get_token(token) 
    splited_token = token.split('-')
    username = splited_token[0]
    tip = int(splited_token[1])
    order_id = int(splited_token[2])
    order = BaseOrder.objects.get(id = order_id)
    booster = splited_token[3]
    payer_id = request.GET.get("PayerID")
    notice = f'Tip from {username}'
    invoice = request.session.get('invoice', 'unknown')
    if request.user == token_with_data.user and request.user.username == username and payer_id:
        room = Room.get_specific_room(request.user, order.name)
        msg = f'{request.user.first_name} Tips {booster} with {tip}$'
        Message.create_tip_message(request.user,msg,room)
        token_with_data.delete()
        if invoice != 'unknown':
            request.session.pop('invoice')
        tip_data = Tip_data.create_tip(invoice, payer_id)
        booster_instance = BaseUser.objects.get(username=booster)
        Transaction.objects.create(user=booster_instance, amount=tip, order_id=order_id, notice=notice, tip=tip_data, status='Tip', type='DEPOSIT')
        booster_wallet = booster_instance.wallet
        booster_wallet.money += tip
        booster_wallet.save()
        return redirect('accounts.customer_side')
    return HttpResponse("error while adding tip to bosster, check your wallet and call page admin")

def cancel_tip(request, token):
    TokenForPay.delete_token(token)
    request.session['success_tip'] = 'false'
    return redirect('accounts.customer_side')

# TODO fix error : order = BaseOrder.objects.filter(customer=customer).last()
@login_required
def customer_side(request, order_name):
    customer = request.user
    base_order = BaseOrder.objects.filter(customer=customer,name=order_name).order_by('id').last()
    if base_order:
        if base_order.is_done:
            return redirect(reverse_lazy('rate.page', kwargs={'order_id': base_order.id}))
        boosters = get_boosters(base_order.game.pk)     
        
        # Chat with admins
        admins_chat_slug = f'roomFor-{request.user.username}-admins-{base_order.name}'

        admins_room = Room.objects.get(slug=admins_chat_slug)
        admins_messages = Message.objects.filter(room=admins_room)

        game_order = base_order.related_order
        
        # Chat with booster
        specific_room = Room.get_specific_room(request.user, base_order.name)
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
                'order':game_order,
                'admins_room':admins_room,
                'admins_room_name':admins_room,
                'admins_messages':admins_messages,
                'admins_chat_slug':admins_chat_slug
            }    
            template_name = 'accounts/customer_side.html'
            return render(request, template_name, context)
        return  HttpResponse("error on creating chat")
    messageForPageResponse.error(request, "This order dosent belong to you, dont try to cheat (:")
    return  redirect(reverse('homepage.index'))


@login_required
def edit_customer_profile(request):
    profile_form = ProfileEditForm(instance=request.user)
    password_form = PasswordEditForm(user=request.user)

    if request.method == 'POST':
        if 'profile_submit' in request.POST:
            profile_form = ProfileEditForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                NotifyMessage.success(request, 'Profile Updated Successfully.')
                return redirect('edit.customer.profile')

        elif 'password_submit' in request.POST:
            password_form = PasswordEditForm(request.user, request.POST)
            if password_form.is_valid():
                password_form.save()
                NotifyMessage.success(request, 'Password Changed Successfully.')
                return redirect('edit.customer.profile')

    return render(request, 'accounts/edit_profile.html', {'profile_form': profile_form, 'password_form': password_form})

@login_required
def customer_history(request):
    history = Transaction.objects.filter(user=request.user)
    return render(request, 'accounts/customer_histoty.html', context={'history' : history})

def payment_canceled(request):
    return HttpResponse('payment canceled')



############### test
# def order_list(request):
#     return render(request, 'accounts/order_list.html')


# def submit_order(request):

#     order_name = 'order by webb b '
#     user = request.user.username

#     BaseOrder.objects.create(status=order_name,user=user)
#     orders = BaseOrder.objects.all().order_by('-timestamp')[:2]
#     all_orders_dict = [
#         {
#             "id": order.pk,
#             'customer': order.customer.username,
#             'status': order.status,
#             'created_at': str(order.created_at),
#         }
#         for order in orders
#     ]
#     async_to_sync(channel_layer.group_send)(
#         'orders',
#         {
#             'type': 'order_list',
#             'order': all_orders_dict,
#         }
#     )

#     return JsonResponse({'message': 'Order submitted successfully'})





# async def create_background_job_to_change_order_price(request, id):    
#     # Run the background task asynchronously
#     asyncio.create_task(my_background_task(id))
#     return redirect(reverse('accounts.customer_side'))
    

# async def my_background_task(id):
#     print(f"Task executed: order_id {id}")
#     delays = [60, 180, 900, 1800]
#     group_name = f"price_updates_{id}"
#     channel_layer = get_channel_layer()
#     async def send_price_update(delay, details):
#         await asyncio.sleep(delay)
#         print(f'price updated ... {delay}')
#         order = await get_order(id)
#         details = await database_sync_to_async(order.update_actual_price)()
#         await channel_layer.group_send(
#             group_name,
#             {
#                 'type': 'update_price',
#                 'price': details['price'],
#                 'time': details['time'],
#             }
#         )
#         for delay in delays:
#                 order = await get_order(id)
#                 details = await database_sync_to_async(order.update_actual_price)()
#                 if details['time'] == -1:
#                     print(f"Breaking loop due to details['time'] = -1")
#                     break
#                 else:
#                     await send_price_update(delay, details)
# 
# 
# @database_sync_to_async
# def get_order(id):
#     return BaseOrder.objects.get(id=id)



def test(request):
    # return render(request, 'accounts/order_list.html')
    return HttpResponse('Done')


class PromoCodeAPIView(APIView):
    def post(self, request):
        code = request.data.get('code', None).lower() 
        if code is None:
            return Response({"error": "Promo code is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            promo_code = PromoCode.objects.get(code=code)
            serializer = PromoCodeSerializer(promo_code)
            if serializer.data['is_active']:
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "Promo Code Is Expired"}, status=status.HTTP_400_BAD_REQUEST)
        except PromoCode.DoesNotExist:
            return Response({"error": "Promo Code Not Found"}, status=status.HTTP_404_NOT_FOUND)