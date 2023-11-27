from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from accounts.forms import  Registeration
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseBadRequest
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils import timezone
from django.contrib.auth.views import LoginView
User = get_user_model()

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



def register_view(request):
    if request.method == 'POST':
        form = Registeration(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            print(user.email_verified_at)
            user.is_active = False  # Mark the user as inactive until they activate their account
            user.save()
            # Send activation email
            send_activation_email(user, request)
            return render(request, 'accounts/activation_sent.html')
    else:
        form = Registeration()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')


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
        return render(request, 'accounts/activation_success.html')
    
    return HttpResponseBadRequest('Activation link is invalid or has expired.')


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html' 
    def get_success_url(self):
        return reverse_lazy('accounts.profile')  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    



