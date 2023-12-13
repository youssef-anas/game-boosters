from django.contrib import admin
from django.urls import path, include
from accounts.views import *

urlpatterns = [
    path('register/', register_view, name='accounts.register'),
    path('profile/', profile_view, name='accounts.profile'),
    path('activate/<str:uidb64>/<str:token>/', activate_account, name='account.activate'),
    path('login/', login_view, name='account.login'),
    path('logout/', logout_view, name='account.logout'), 
    path('choose_booster/', choose_booster, name='choose.booster'),
    path('set_customer_data/', set_customer_data, name='set.customer.data'),
    path('customer_side/<int:id>/<slug:admins_chat_slug>/', customer_side, name='accounts.customer_side')
]