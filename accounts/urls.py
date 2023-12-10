from django.contrib import admin
from django.urls import path, include
from accounts.views import register_view, profile_view, activate_account, login_view, logout_view, order_view, choose_booster, set_customer_data, customer_side

urlpatterns = [
    path('register/', register_view, name='accounts.register'),
    path('profile/', profile_view, name='accounts.profile'),
    path('order/<int:id>', order_view, name='customer.order'),
    path('activate/<str:uidb64>/<str:token>/', activate_account, name='account.activate'),
    path('login/', login_view, name='account.login'),
    path('logout/', logout_view, name='account.logout'), 
    path('choose_booster/', choose_booster, name='choose.booster'),
    path('set_customer_data/', set_customer_data, name='set.customer.data'),
    path('customer_side/', customer_side, name='accounts.customer_side')
]