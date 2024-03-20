from django.urls import path
from csgo2.views import *

urlpatterns = [
  path('', csgo2GetBoosterByRank, name='csgo2'),
  path('paypal/', pay_with_paypal, name='csgo2-paypal-redirect'),
  path('cryptomus/', pay_with_cryptomus, name='csgo2-cryptomus-redirect'),
]