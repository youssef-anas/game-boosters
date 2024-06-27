from django.contrib import admin
from django.urls import path, include
from accounts.views import *

urlpatterns = [
    path('signup/',create_account, name='accounts.signup'),
    path('logout/', CustomLogoutView.as_view(), name='account.logout'), 
    path('login/', CustomLoginView.as_view(), name='account.login'),
    path('activate/sent/', activate_account_sent, name='accounts.activate.sent'),
    path('activate/<int:code>/',activate_account, name='accounts.activate.code'),
    path('promo-codes/', PromoCodeAPIView.as_view(), name='promo_code_detail'),
    
    path('password/reset/', reset_password_request, name='password.reset'),
    path('password/check-code/<int:id>/', check_reset_code, name='password.check.code'),
    path('password/change/<int:id>/', change_password_page, name='password.change'),
    path('add/images/', list_blobs, name='.change'),
    path('delete/images/', delete_public_images, name='.change'),
    # path('message/', test_email_view, name='.change'),
    # path('img/', generate_captcha_image, name='generate_captcha_image'),
]