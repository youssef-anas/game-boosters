from django.contrib import admin
from django.urls import path
from wildRift.views import *

urlpatterns = [

    path('divisions-data/', get_wildrift_divisions_data_view, name='get_wildrift_divisions_data'),
    path('marks-data/', get_wildrift_marks_data_view, name='get_wildrift_marks_data'),


    path('', wildRiftGetBoosterByRank, name='wildRift'),
    path('payment/', WRPaymentAPiView.as_view(), name='wildRift-paypal-redirect'),
]
