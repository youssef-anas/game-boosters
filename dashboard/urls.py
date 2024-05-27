from django.contrib import admin
from django.urls import path
from dashboard.views import admin_side

urlpatterns = [
    path('chat/<str:order_name>/', admin_side, name='admin_side'),
]
