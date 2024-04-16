from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from customer.forms import Registeration
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse
from django.utils import timezone
from django.contrib.auth import login
from accounts.models import BaseUser, PromoCode
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import PromoCodeSerializer
from datetime import timedelta
from django.contrib.auth.views import LoginView
from gameBoosterss.utils import send_activation_code, reset_password
from accounts.forms import EmailForm, ResetCodeForm, PasswordChangeCustomForm
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import View
from django.utils.translation import gettext_lazy as _


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('homepage.index')
    redirect_authenticated_user = True

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
        form = Registeration(request.POST,request.FILES)
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
    form =  Registeration()
    return render(request, 'accounts/register.html', {'form': form})


def activate_account_sent(request):
    email = request.session.get('email')
    return render(request, 'accounts/activation_sent.html', context={'email':email})


def activate_account(request, code):
    user = BaseUser.objects.get(activation_code=code)

    if not user:
        messages.error(request, 'Error in code')
        return redirect(reverse('accounts.activate.sent'))

    time_difference = timezone.now() - user.activation_time
    if time_difference > timedelta(minutes=1):
        return HttpResponseBadRequest("Activation time hasn't elapsed yet")

    user.is_active = True
    user.activation_code = None
    user.save()

    # Set the backend attribute on the user
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    request.session.pop('email', None)

    messages.success(request, 'Your account has been activated successfully')
    return redirect(reverse_lazy('homepage.index'))


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
    if request.method == 'POST':
        form = ResetCodeForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            if user.rest_password_code == form.cleaned_data['reset_code']:
                user.rest_password_code = None
                user.save()
                return redirect(reverse_lazy('password.change', kwargs={'id': user.id}))
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
            return redirect(reverse_lazy('account_login'))
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
