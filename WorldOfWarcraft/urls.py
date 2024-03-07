from django.urls import path
from WorldOfWarcraft.views import *

urlpatterns = [
  path('', wowGetBoosterByRank, name='wow'),
  path('paypal/', pay_with_paypal, name='wow-paypal-redirect'),
  path('cryptomus/', pay_with_cryptomus, name='wow-cryptomus-redirect'),
]