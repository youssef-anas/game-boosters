from django.urls import path
from .views import *

urlpatterns = [
  path('get-divisions-data/', get_divisions_data_view, name='get-divisions-data'),
  path('get-marks-data/', get_marks_data_view, name='get-marks-data'),  

  path('', pubgGetBoosterByRank, name='pubg'),
  path('paypal/', view_that_asks_for_money, name='pubg-paypal-redirect'),
]