from django.contrib import admin
from django.urls import path
from wildRift.views import *

urlpatterns = [
    path('', wildRiftGetBoosterByRank,name='wildrift'),
    path('paypal/', view_that_asks_for_money, name='wildrift-paypal-redirect'),
    # path('payment-successed/', payment_successed ,name='wildrift.payment.success'),
    path('payment-canceled/', payment_canceled ,name='wildrift.payment.canceled'),
    path('orders/', wildRiftOrders ,name='wildrift.confirm.order'),
    path('<order_type>/<int:id>/', wildRiftOrderChat, name='order.chat'),
    # path('paypal-ipn/', paypal_ipn_listener, name='paypal-ipn'),
]
