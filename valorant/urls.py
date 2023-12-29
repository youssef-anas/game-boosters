from django.contrib import admin
from django.urls import path
from valorant.views import *

urlpatterns = [
  path('', valorantGetBoosterByRank, name='valorant')
]
