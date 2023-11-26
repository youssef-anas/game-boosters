from django.contrib import admin
from django.urls import path
from wildRift.views import wildRiftGetBoosterByRank

urlpatterns = [
    path('', wildRiftGetBoosterByRank,name='wildrift')
]
