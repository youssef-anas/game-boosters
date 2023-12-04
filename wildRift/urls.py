from django.contrib import admin
from django.urls import path
from wildRift.views import wildRiftGetBoosterByRank, view_that_asks_for_money, payment_canceled, payment_successed, wildRiftOrders, wildRiftOrderChat

urlpatterns = [
    path('', wildRiftGetBoosterByRank,name='wildrift'),
    path('paypal/', view_that_asks_for_money ,name='paypal'),
    path('payment-successed/', payment_successed ,name='wildrift.payment.success'),
    path('payment-canceled/', payment_canceled ,name='wildrift.payment.canceled'),
    path('orders/', wildRiftOrders ,name='wildrift.confirm.order'),
    path('<order_type>/<int:id>/', wildRiftOrderChat, name='order.chat'),
]
