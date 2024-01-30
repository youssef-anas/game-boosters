from django.contrib import admin
from django.urls import path
from rocketLeague.views import *

urlpatterns = [
  path('', rocketLeagueGetBoosterByRank, name='rocketLeague'),
  path('paypal/', view_that_asks_for_money, name='rocketLeague-paypal-redirect'),
  path('payment-canceled/', payment_canceled ,name='rocketLeague.payment.canceled'),
]