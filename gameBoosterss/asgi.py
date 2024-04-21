import os
import django

# Manually configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameBoosterss.settings')
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path, re_path
from chat.consumers import ChatConsumer
from accounts.consumers import OrderConsumer, PriceConsumer

websocket_urlpatterns = [
    ] 

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                re_path(r'ws/chat/(?P<room_slug>[^/]+)/$', ChatConsumer.as_asgi()),
                re_path(r'ws/order/$', OrderConsumer.as_asgi()),
                re_path(r'ws/price/(?P<order_id>\d+)/$', PriceConsumer.as_asgi()),
            ])
        ),
    ),
})