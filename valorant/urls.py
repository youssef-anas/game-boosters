from django.contrib import admin
from django.urls import path
from valorant.views import *

urlpatterns = [
  path('divisions-data/', valorant_divisions_data, name='valorant_divisions_data'),
  path('marks-data/', valorant_marks_data, name='valorant_marks_data'),
  path('placements-data/', valorant_placements_data, name='valorant_placements_data'),  

  path('', valorantGetBoosterByRank, name='valorant'),
  path('paypal/', pay_with_paypal, name='valorant-paypal-redirect'),
  path('cryptomus/', pay_with_cryptomus, name='valorant-cryptomus-redirect'),
]
