from django.contrib import admin
from django.urls import path
from leagueOfLegends.views import *

urlpatterns = [
  path('divisions-data/', get_lol_divisions_data_view, name='leagueOfLegends.getDivisionsData'),
  path('marks-data/', get_lol_marks_data_view, name='leagueOfLegends.getMarksData'),
  path('placements-data/', get_lol_placements_data_view, name='leagueOfLegends.getPlacementsData'),    


  path('', leagueOfLegendsGetBoosterByRank, name='lol'),
  path('paypal/', pay_with_paypal, name='lol-paypal-redirect'),
  path('cryptomus/', pay_with_cryptomus, name='lol-cryptomus-redirect'),
]