from django.contrib import admin
from django.urls import path
from valorant.views import *

urlpatterns = [
  path('', valorantGetBoosterByRank, name='valorant'),
  path('paypal/', view_that_asks_for_money, name='valorant-paypal-redirect'),
  path('payment-canceled/', payment_canceled ,name='valorant.payment.canceled'),
]
