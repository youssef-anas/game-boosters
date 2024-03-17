from django.contrib import admin
from django.urls import path
from leagueOfLegends.views import *

urlpatterns = [
  path('', leagueOfLegendsGetBoosterByRank, name='lol'),
  path('paypal/', pay_with_paypal, name='lol-paypal-redirect'),
  path('cryptomus/', pay_with_cryptomus, name='lol-cryptomus-redirect'),
]