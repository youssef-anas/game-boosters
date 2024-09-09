from django.contrib import admin
from django.urls import path
from leagueOfLegends.views import *

urlpatterns = [
  path('divisions-data/', get_lol_divisions_data_view, name='leagueOfLegends.getDivisionsData'),
  path('marks-data/', get_lol_marks_data_view, name='leagueOfLegends.getMarksData'),
  path('placements-data/', get_lol_placements_data_view, name='leagueOfLegends.getPlacementsData'),    


  path('', leagueOfLegendsGetBoosterByRank, name='lol'),
  path('payment/', LOLPaymentAPiView.as_view(), name='lol-paypal-redirect'),
]