from django.contrib import admin
from django.urls import path
from tft.views import *

urlpatterns = [
  path('', tftGetBoosterByRank, name='tft'),
  path('division/', get_tft_divisions_data_view, name='tft-division'),
  path('marks/', get_tft_marks_data_view, name='tft-marks'),

  path('paypal/', TFTPaymentAPiView.as_view(), name='tft-paypal-redirect'),
]