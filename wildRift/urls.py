from django.contrib import admin
from django.urls import path
from wildRift.views import *

urlpatterns = [
    path('', wildRiftGetBoosterByRank, name='wildRift'),
    path('paypal/', view_that_asks_for_money, name='wildRift-paypal-redirect'),
    path('payment-canceled/', payment_canceled ,name='wildRift.payment.canceled'),
]
