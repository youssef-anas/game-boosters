from django.urls import path
from csgo2.views import *

urlpatterns = [
  path('division-prices/', get_division_prices_view, name='csgo2-division-prices'),
  path('premier-prices/', get_premier_prices_view, name='csgo2-premier-prices'),
  path('faceit-prices/', get_faceit_prices_view, name='csgo2-faceit-prices'),

  path('', csgo2GetBoosterByRank, name='csgo2'),
  path('payment/', CSGO2PaymentAPiView.as_view(), name='csgo2-paypal-redirect'),
]