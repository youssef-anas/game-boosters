from django.contrib import admin
from django.urls import path, include
from accounts.views import *
from django.contrib.auth.decorators import user_passes_test

def is_customer(user):
    return user.is_authenticated and (user.is_customer or not user.is_booster)

urlpatterns = [
    path('register/', register_view, name='accounts.register'),
    path('profile/', profile_view, name='accounts.profile'),
    path('activate/<str:uidb64>/<str:token>/', activate_account, name='account.activate'),
    path('login/', login_view, name='account.login'),
    path('logout/', logout_view, name='account.logout'), 
    path('choose_booster/', choose_booster, name='choose.booster'),
    path('set_customer_data/', set_customer_data, name='set.customer.data'),
    path('tip_booster/', tip_booster, name='tip_booster'),
    path('tip_booster/success/', success_tip, name='tip_booster.success_tip'),
    path('tip_booster/cancel/', cancel_tip, name='tip_booster.cancel_tip'),
    path('customer_side/', user_passes_test(is_customer)(customer_side), name='accounts.customer_side'),
    path('edit_profile/', user_passes_test(is_customer)(edit_customer_profile), name='edit.customer.profile'),
]