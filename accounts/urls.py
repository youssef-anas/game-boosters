from django.contrib import admin
from django.urls import path, include
from accounts.views import register_view, profile_view, activate_account, login_view, logout_view

urlpatterns = [
    path('register/', register_view, name='accounts.register'),
    path('profile/', profile_view, name='accounts.profile'),
    path('activate/<str:uidb64>/<str:token>/', activate_account, name='account.activate'),
    path('login/', login_view, name='account.login'),
    path('logout/', logout_view, name='account.logout'), 
]