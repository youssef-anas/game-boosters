from django.contrib import admin
from django.urls import path
from booster.views import *

urlpatterns = [
    path('register/',register_booster_view,name='booster.register'),
    path('profile/',profile_booster_view,name='booster.profile'),
    path('orders/',booster_orders,name='booster.orders'),
    path('update-rating/',update_rating,name='order.update.rating'),
    path('upload-image/',upload_finish_image,name='order.upload.image'),
]
