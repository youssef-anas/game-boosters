from django.contrib import admin
from django.urls import path
from honorOfKings.views import *

urlpatterns = [
  path('', honerOfKingeGetBoosterByRank, name='hok'),
  path('paypal/', pay_with_paypal, name='hok-paypal-redirect'),
  path('cryptomus/', pay_with_cryptomus, name='hok-cryptomus-redirect'),
]