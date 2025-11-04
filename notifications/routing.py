from django.urls import re_path
from .consumers import NotificationsConsumer

websocket_urlpatterns = [
    re_path(r"ws/notifications/(?P<user_role>[^/]+)/$", NotificationsConsumer.as_asgi()),
]



