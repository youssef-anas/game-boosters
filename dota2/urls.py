from django.urls import path
from .views import *

urlpatterns = [
  path('', dota2GetBoosterByRank, name='dota2'),
  path('paypal/', view_that_asks_for_money, name='dota2-paypal-redirect'),
  path('payment-canceled/', payment_canceled ,name='dota2.payment.canceled'),
]