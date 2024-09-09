from django.contrib import admin
from django.urls import path
from tft.views import *

urlpatterns = [
  path('', tftGetBoosterByRank, name='tft'),
  path('paypal/', TFTPaymentAPiView.as_view(), name='tft-paypal-redirect'),
]