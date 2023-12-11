from django.contrib import admin
from django.urls import path
from booster.views import *

urlpatterns = [
    path('register/',register_booster_view,name='booster.register'),
    path('profile/',profile_booster_view,name='booster.profile'),
    path('rate/<int:order_id>/',get_rate,name='booster.rate'), # form to get rate if order done
    path('form_test/', form_test, name='form_test'), # test page , only for test
]
