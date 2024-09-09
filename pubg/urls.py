from django.urls import path
from .views import *

urlpatterns = [
  path('get-divisions-data/', get_divisions_data_view, name='get-divisions-data'),
  path('get-marks-data/', get_marks_data_view, name='get-marks-data'),  

  path('', pubgGetBoosterByRank, name='pubg'),
  path('payment/', PubgPaymentAPiView.as_view(), name='pubg-paypal-redirect'),
]