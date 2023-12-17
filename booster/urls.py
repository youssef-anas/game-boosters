from django.contrib import admin
from django.urls import path
from booster.views import *

urlpatterns = [
    path('register/',register_booster_view,name='booster.register'),
    path('edit_profile/', edit_booster_profile, name='edit.booster.profile'),
    path('profile/<booster_id>/',profile_booster_view,name='booster.profile'),
    path('rate/<int:order_id>/',get_rate,name='booster.rate'), # form to get rate if order done
    path('form_test/', form_test, name='form_test'), # test page , only for test
    path('orders/',booster_orders,name='booster.orders'),
    path('update-rating/',update_rating,name='order.update.rating'),
    path('upload-image/',upload_finish_image,name='order.upload.image'),
    path('drop-order/',drop_order,name='drop.order'),
    path('confirm_details/',confirm_details,name='confirm.details'),
    path('ask_customer/',ask_customer,name='ask.customer'),
    path('can_choose_me/', CanChooseMe.as_view(), name='can_choose_me'),
]
