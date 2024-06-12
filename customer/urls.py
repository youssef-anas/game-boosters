from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth.decorators import user_passes_test


def is_customer(user):
    return user.is_authenticated and (user.is_customer or not user.is_booster)

urlpatterns = [
    path('customer_orders/', user_passes_test(is_customer)(customer_orders), name='customer.orders'),

    path('customer_orders/<str:order_name>/', user_passes_test(is_customer)(customer_side), name='customer.orders.details'),
    path('customer_orders/fill-data/<str:order_name>/', BaseOrderFormView.as_view(), name='customer.filldata'),

    path('payment-success/<str:token>/', payment_sucess_view, name='payment.success'),
    path('payment-canceled/<str:token>/', payment_canceled ,name='payment.canceled'),

    path('tip-booster/', tip_booster, name='tip_booster'),
    path('tip-booster/success/<str:token>/', success_tip, name='tip_booster.success_tip'),
    path('tip-booster/cancel/<str:token>/<int:order_id>', cancel_tip, name='tip_booster.cancel_tip'),

    path('choose_booster/<int:order_id>/<int:booster_id>', choose_booster, name='choose.booster'),
    path('set_customer_data/', set_customer_data, name='set.customer.data'),

    path('profile_setting/', user_passes_test(is_customer)(customer_setting), name='customer.setting'),

    path('custome_order/<int:game_id>', user_passes_test(is_customer)(custom_order), name='custom.order'),

    path('available/<int:id>/', AvailableToPlayMail.as_view(), name='available'),
]
