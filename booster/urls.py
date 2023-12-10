from django.contrib import admin
from django.urls import path
from booster.views import register_booster_view, profile_booster_view, booster_orders

urlpatterns = [
    path('register/',register_booster_view,name='booster.register'),
    path('profile/',profile_booster_view,name='booster.profile'),
    path('orders/',booster_orders,name='booster.orders'),
]
