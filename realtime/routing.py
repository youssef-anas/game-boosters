from django.urls import re_path
from realtime import consumers

websocket_urlpatterns = [
    re_path(r'ws/orders/(?P<order_id>\d+)/$', consumers.OrderSyncConsumer.as_asgi()),
]



