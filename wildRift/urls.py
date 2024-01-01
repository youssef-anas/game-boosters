from django.contrib import admin
from django.urls import path
from wildRift.views import *

urlpatterns = [
    path('', wildRiftGetBoosterByRank, name='wildrift'),
    path('paypal/', view_that_asks_for_money, name='wildrift-paypal-redirect'),
    # path('payment-successed/', payment_successed ,name='wildrift.payment.success'),
    path('payment-canceled/', payment_canceled ,name='wildrift.payment.canceled'),
    # path('paypal-ipn/', paypal_ipn_listener, name='paypal-ipn'),
    path('get_latest_price/', get_latest_price, name='get_latest_price'),
    path('update-rating/',update_rating,name='order.update.rating'),
    path('upload-image/',upload_finish_image,name='order.upload.image'),
    path('drop-order/',drop_order,name='drop.order'),
    path('confirm_details/',confirm_details,name='confirm.details'),
    path('ask_customer/',ask_customer,name='ask.customer'),
]
