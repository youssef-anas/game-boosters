import os
from django.core.asgi import get_asgi_application
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameBoosterss.settings')
 
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter , URLRouter
from chat import routing as chatRouting
from accounts.controller import routing as orderRouting
application = ProtocolTypeRouter(
    {
        "http" : get_asgi_application() ,
        "websocket" : AuthMiddlewareStack(
            URLRouter(
                orderRouting.websocket_urlpatterns + chatRouting.websocket_urlpatterns
            )   
        )
    }
)