from django.urls import path
from overwatch2.views import *

urlpatterns = [
  path('divisions-data/', get_overwatch2_divisions, name='overwatch2_divisions_data'),
  path('marks-data/', get_overwatch2_marks, name='overwatch2_marks_data'),
  path('placements-data/', get_overwatch2_placements, name='overwatch2_placements_data'),  


  path('', overwatch2GetBoosterByRank, name='overwatch2'),
  path('paypal/', view_that_asks_for_money, name='overwatch2-paypal-redirect'),
  path('cryptomus/', view_that_asks_for_money, name='overwatch2-cryptomus-redirect'),
]