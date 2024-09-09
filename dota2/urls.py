from django.urls import path
from .views import *

urlpatterns = [
  path('division-prices/', division_prices_view, name='dota2-division-prices'),
  path('placement-prices/', placement_prices_view, name='dota2-placement-prices'),

  path('', dota2GetBoosterByRank, name='dota2'),
  path('payment/', DOTA2PaymentAPiView.as_view(), name='dota2-paypal-redirect'),
]