from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from accounts.forms import  Registeration
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

User = get_user_model()

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


@csrf_exempt
def register_view(request):
    payer_id = request.GET.get('PayerID')
    order_id = request.GET.get('order_id')
    order = get_object_or_404(WildRiftDivisionOrder, id=order_id)
    if order.customer:
        return HttpResponse('this order with another user, create order again or connect to admin')
    if request.user.is_authenticated:   
        order.customer = request.user
        order.save()
        return render(request, 'accounts/customer_side.html')
    if request.method == 'POST':
        form = Registeration(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            order.customer = user
            order.save()
            login(request, user)
            # Send activation email
            # send_activation_email(user, request)
            # return render(request, 'accounts/activation_sent.html')
            return render(request, 'accounts/customer_side.html')
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
            return redirect(reverse_lazy('accounts.profile'))
        else:
            # Authentication failed, handle it as needed
            context = {'error_message': 'Invalid Credentials'}
            return render(request, template_name, context)
    return render(request, template_name)
    
def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('homepage.index'))

def order_view(request, id):
    if request.user.is_authenticated:
        try:
            order = WildRiftDivisionOrder.objects.get(id=id, customer=request.user, )
            return render(request, 'accounts/customer_side.html', context={'order': order})
        except WildRiftDivisionOrder.DoesNotExist:
            return HttpResponse("Order Not Found For The Current User And Order ID.")
    else:
        return HttpResponse("User Not Authenticated.")
