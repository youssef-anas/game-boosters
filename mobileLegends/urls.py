from django.urls import path
from mobileLegends.views import *

urlpatterns = [
  path('divisions-data/', get_mobile_legends_divisions_view, name='get_mobile_legends_divisions'),
  path('marks-data/', get_mobile_legends_marks_view, name='get_mobile_legends_marks'),
  path('placements-data/', get_mobile_legends_placements_view, name='get_mobile_legends_placements'),  

  path('', MobileLegendsGetBoosterByRank, name='mobileLegends'),
  path('payment/', MobLegPaymentAPiView.as_view(), name='mobileLegends-paypal-redirect'),
]
