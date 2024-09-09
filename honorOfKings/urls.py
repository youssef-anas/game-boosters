from django.contrib import admin
from django.urls import path
from honorOfKings.views import *

urlpatterns = [
  path('divisions-data/', get_hok_divisions_data_view, name='honorOfKings.getDivisionsData'),
  path('marks-data/', get_hok_marks_data_view, name='honorOfKings.getMarksData'),    

  path('', honerOfKingeGetBoosterByRank, name='hok'),
  path('payment/', HOKPaymentAPiView.as_view(), name='hok-paypal-redirect'),
]