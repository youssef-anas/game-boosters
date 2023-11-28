from django.contrib import admin
from django.urls import path
from wildRift.views import wildRiftGetBoosterByRank, view_that_asks_for_money

urlpatterns = [
    path('', wildRiftGetBoosterByRank,name='wildrift'),
    path('paypal/', view_that_asks_for_money ,name='paypal'),
]
