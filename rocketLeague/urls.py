from django.contrib import admin
from django.urls import path
from rocketLeague.views import *

urlpatterns = [
  path('divisions-data/', rocket_league_divisions_data_api, name='rocket_league_divisions_data_api'),
  path('placements-data/', rocket_league_placements_data_api, name='rocket_league_placements_data_api'),
  path('seasonals-data/', rocket_league_seasonals_data_api, name='rocket_league_seasonals_data_api'),
  path('tournaments-data/', rocket_league_tournaments_data_api, name='rocket_league_tournaments_data_api'),


  path('', rocketLeagueGetBoosterByRank, name='rocketLeague'),
  path('paypal/', pay_with_paypal, name='rocketLeague-paypal-redirect'),
  path('cryptomus/', pay_with_cryptomus, name='rocketLeague-cryptomus-redirect'),
]