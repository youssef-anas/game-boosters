from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from customer.forms import Registration
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse
from django.utils import timezone
from django.contrib.auth import login
from accounts.models import BaseUser, PromoCode, BaseOrder
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import PromoCodeSerializer
from datetime import timedelta
from django.contrib.auth.views import LoginView
from gameBoosterss.utils import send_activation_code, reset_password
from accounts.forms import EmailForm, ResetCodeForm, PasswordChangeCustomForm, LoginForm
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import View
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm



class CustomLoginForm(AuthenticationForm):
    # Customize your login form as needed
    pass

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('homepage:index')
    redirect_authenticated_user = True
    authentication_form = LoginForm 

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs())
    
    def form_invalid(self, form):
        
        # Re-render the form with errors
        return self.render_to_response(self.get_context_data(form=form))
    

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_booster:
            # if not self.request.user.booster.profile_completed():
            #     messages.error(self.request, 'Please complete your profile first!')
            #     return redirect('booster.setting')
            messages.success(self.request, 'Welcome back!')
            return redirect('booster.orders')
        return response

class CustomLogoutView(View):
    redirect_url = reverse_lazy('homepage.index')

    def get(self, request, *args, **kwargs):
        """Logout via GET request."""
        logout(request)
        return redirect(self.redirect_url)

def create_account(request):
    email = request.session.get('email')
    if email:
        user = get_object_or_404(BaseUser, email = email)
        send_activation_code(user)
        return redirect('accounts.activate.sent')
    if request.method == 'POST':
        form = Registration(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            # profile_image = form.cleaned_data['profile_image']
            # image_name = f"accounts/images/{profile_image.name}"
            # image_data = profile_image.read()
            # upload_image_to_firebase(image_data=image_data, filename=image_name)
            # user.profile_image = image_name
            user.save()
            send_activation_code(user)
            request.session['email'] = user.email
            return redirect('accounts.activate.sent')
        else:
            return render(request, 'accounts/register.html', {'form': form})
    form =  Registration()
    return render(request, 'accounts/register.html', {'form': form})


def activate_account_sent(request):
    email = request.session.get('email')
    return render(request, 'accounts/activation_sent.html', context={'email':email})


def activate_account(request, code):
    try :
        user = BaseUser.objects.get(activation_code=code)

        time_difference = timezone.now() - user.activation_time
        if time_difference > timedelta(minutes=20):
            messages.error(request, "Activation time hasn't elapsed yet")
            return redirect(reverse('accounts.activate.sent'))

        user.is_active = True
        user.activation_code = None
        user.save()

        # Set the backend attribute on the user
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        request.session.pop('email', None)

        messages.success(request, 'Your account has been activated successfully')
        return redirect(reverse_lazy('homepage.index'))
    
    except BaseUser.DoesNotExist:
        # Handle invalid code
        messages.error(request, 'Invalid code')
        return redirect(reverse('accounts.activate.sent'))


def reset_password_request(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = get_object_or_404(BaseUser, email=email)
            reset_password(user)
            return render(request, 'accounts/password_reset/reset_code.html', {'user': user})
    else:
        form = EmailForm()
    return render(request, 'accounts/password_reset/reset_password.html', {'form': form})


def check_reset_code(request, id):
    user = get_object_or_404(BaseUser, id=id)
    print(user, request.method)
    if request.method == 'POST':
        form = ResetCodeForm(request.POST)
        if form.is_valid():
            if user.rest_password_code == form.cleaned_data['reset_code']:
                user.rest_password_code = None
                user.save()
                return redirect(reverse_lazy('password.change', kwargs={'id': user.id}))
            else:
                messages.error(request, 'Invalid code')
                return redirect(reverse_lazy('password.check.code', kwargs={'id': user.id}))
        else:
            messages.error(request, 'Invalid code')
            return redirect(reverse_lazy('password.check.code', kwargs={'id': user.id}))
    form = ResetCodeForm()        
    return render(request, 'accounts/password_reset/reset_code.html', context={'user':user, 'form':form})


def change_password_page(request, id):
    user = get_object_or_404(BaseUser, id=id)
    
    if request.method == 'POST':
        form = PasswordChangeCustomForm(user=user, data=request.POST)
        if form.is_valid():
            password = form.cleaned_data['new_password1']
            user.set_password(password)
            user.reset_password_code = None
            user.save()
            # Set the backend attribute on the user
            # user.backend = 'django.contrib.auth.backends.ModelBackend'
            # login(request, user)
            messages.success(request, 'Password reset successfully.')
            return redirect(reverse_lazy('account.login'))
    else:
        form = PasswordChangeCustomForm(user=user)
    
    return render(request, 'accounts/password_reset/change_password.html', {'form': form})


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


from firebase_admin import storage
from gameBoosterss.utils import upload_image_to_firebase
from rest_framework.decorators import api_view

@api_view(['POST'])
def list_blobs(request):
    imgs = request.FILES.getlist('imgs')
    path = request.data.get('path')
    for img in imgs:
        # Assuming upload_image_to_firebase is a function that uploads the image to Firebase Storage
        blob_url = upload_image_to_firebase(img, path+'/'+img.name)
        print("done", img.name)
    return HttpResponse("all done")

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def delete_public_images(request):
    if request.method == 'POST':
        path = request.POST.get('path')

        # Reference the Firebase Storage bucket
        bucket = storage.bucket()

        # List all files in the specified path
        blobs = bucket.list_blobs(prefix=path)

        # Iterate through the blobs and delete public images
        deleted_images = []
        for blob in blobs:
            if blob.public_url:
                blob.delete()
                deleted_images.append(blob.public_url)

        return JsonResponse({'message': 'Public images deleted successfully', 'deleted_images': deleted_images})

    else:
        return JsonResponse({'error': 'POST method required'}, status=400)
    


from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render

def test_email_view(request):
    subject = 'Test Email'
    message = 'This is a test email sent from Django.'
    from_email = 'customerservice@madboost.gg'
    to_email = ['shethr999@gmail.com']

    try:
        send_mail(subject, message, from_email, to_email)
        return HttpResponse('Email sent successfully!')
    except Exception as e:
        return HttpResponse('An error occurred: {}'.format(str(e)))


from django.http import HttpResponse
from PIL import Image, ImageDraw, ImageFont
import random
import io, string, os
from django.core.files.base import ContentFile
from accounts.models import Captcha

def generate_random_value():
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    digits = string.digits
    
    # Generate 3 random uppercase letters
    uppercase_chars = ''.join(random.choices(uppercase_letters, k=2))
    
    # Generate 1 random lowercase letter
    lowercase_char = random.choice(lowercase_letters)
    
    # Generate 1 random digit
    digit = random.choice(digits)
    
    # Combine and shuffle
    value = uppercase_chars + lowercase_char + digit
    value_list = list(value)
    random.shuffle(value_list)
    
    return ''.join(value_list)

def generate_captcha_image(request):
    # static_folder = "static/captcha_images/"
    # os.makedirs(static_folder, exist_ok=True)

    # for _ in range(1000):
    #     value = generate_random_value()

    #     # Generate the image
    #     width, height = 200, 100
    #     image = Image.new("RGB", (width, height), color=(255, 255, 255))
    #     draw = ImageDraw.Draw(image)

    #     # Add text to the image
    #     font_size = 30
    #     font = ImageFont.truetype("arial.ttf", font_size)
    #     text_bbox = draw.textbbox((0, 0), value, font=font)
    #     text_position = ((width - text_bbox[2]) // 2, (height - text_bbox[3]) // 2)
    #     draw.text(text_position, value, fill="black", font=font)

    #     # Save image to static folder
    #     image_path = os.path.join(static_folder, f"{value}.png")
    #     image.save(image_path)

    #     # Save image path to model
    #     Captcha.objects.create(value=value, image=image_path)

    return HttpResponse("Images generated and saved successfully.")