from django.contrib import admin
from django.urls import path
from hearthstone.views import *

urlpatterns = [
  path('divisions-data/', get_hearthstone_divisions_data_view, name='hearthstone.getDivisionsData'),
  path('marks-data/', get_hearthstone_marks_data_view, name='hearthstone.getMarksData'),

  path('', hearthstoneGetBoosterByRank, name='hearthstone'),
  path('payment/', HearthstonePaymentAPiView.as_view(), name='hearthstone-paypal-redirect'),
]