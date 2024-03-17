from django.contrib import admin
from django.urls import path
from tft.views import *

urlpatterns = [
  path('', tftGetBoosterByRank, name='tft'),
  path('paypal/', pay_with_paypal, name='tft-paypal-redirect'),
  path('cryptomus/', pay_with_cryptomus, name='tft-cryptomus-redirect'),
]