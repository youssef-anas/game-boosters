from django.urls import path
from csgo2.views import *

urlpatterns = [
  path('division-prices/', get_division_prices_view, name='csgo2-division-prices'),
  path('premier-prices/', get_premier_prices_view, name='csgo2-premier-prices'),
  path('faceit-prices/', get_faceit_prices_view, name='csgo2-faceit-prices'),

  path('', csgo2GetBoosterByRank, name='csgo2'),
  path('paypal/', pay_with_paypal, name='csgo2-paypal-redirect'),
  path('cryptomus/', pay_with_cryptomus, name='csgo2-cryptomus-redirect'),
]