from django.contrib import admin
from django.urls import path
from booster.views import *
from django.contrib.auth.decorators import user_passes_test

def is_booster(user):
    return user.is_authenticated and user.is_booster

urlpatterns = [
    path('register/',register_booster_view,name='booster.register'),
    path('edit_profile/', edit_booster_profile, name='edit.booster.profile'),
    path('profile/<booster_id>/',user_passes_test(is_booster)(profile_booster_view),name='booster.profile'),
    path('rate/<int:order_id>/',get_rate,name='booster.rate'), # form to get rate if order done
    path('rating/<int:order_id>/', rate_page, name='rate.page'), # test page , only for test
    path('orders/', user_passes_test(is_booster)(booster_orders), name='booster.orders'),
    path('history/', user_passes_test(is_booster)(booster_history), name='booster.history'),
    path('can_choose_me/', CanChooseMe.as_view(), name='can_choose_me'),
    path('jobs/', jobs ,name='orders.jobs'),
    path('<str:game_name>/<int:id>/', calmOrder, name='calm.order'),
]
