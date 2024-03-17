from django.urls import path
from csgo2.views import *

urlpatterns = [
  path('', csgo2GetBoosterByRank, name='csgo2'),
  path('paypal/', view_that_asks_for_money, name='csgo2-paypal-redirect'),
]