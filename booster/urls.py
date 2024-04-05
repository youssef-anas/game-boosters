from django.contrib import admin
from django.urls import path
from booster.views import *
from django.contrib.auth.decorators import user_passes_test

def is_booster(user):
    return user.is_authenticated and user.is_booster

urlpatterns = [
    path('register/',register_booster_view,name='booster.register'),
    path('edit_profile/', edit_booster_profile, name='edit.booster.profile'),
    path('boosters/', boosters, name='booster.boosters'),
    path('boosters/<booster_id>/',booster_details,name='booster.details'),
    path('rate/<int:order_id>/',get_rate,name='booster.rate'), # form to get rate if order done
    path('rating/<int:order_id>/', rate_page, name='rate.page'), # test page , only for test
    path('orders/', user_passes_test(is_booster)(booster_orders), name='booster.orders'),
    path('history/', user_passes_test(is_booster)(booster_history), name='booster.history'),
    path('can_choose_me/', CanChooseMe.as_view(), name='can_choose_me'),
    path('orders_jobs/', orders_jobs ,name='orders.jobs'),
    path('orders_jobs/<str:game_name>/<int:id>/', calm_order, name='calm.order'),
    path('alert_customer/<int:order_id>/',alert_customer, name='alert.customer'),
    path('upload-image/',upload_finish_image,name='order.upload.image'),
    path('drop-order/<int:order_id>',drop_order,name='drop.order'),
    path('update-rating/<int:order_id>',update_rating,name='order.update.rating'),
    path('transactions/',TransactionListView.as_view(),name='booster.transaction'),

]
