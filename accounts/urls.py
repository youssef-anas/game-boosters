from django.contrib import admin
from django.urls import path, include
from accounts.views import *

urlpatterns = [
    path('register/', register_view, name='accounts.register'),
    path('profile/', profile_view, name='accounts.profile'),
    path('activate/<str:uidb64>/<str:token>/', activate_account, name='account.activate'),
    path('login/', login_view, name='account.login'),
    path('logout/', logout_view, name='account.logout'), 
    path('customer_side/', customer_side, name='accounts.customer_side')
]