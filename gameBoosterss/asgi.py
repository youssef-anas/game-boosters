import os
from django.core.asgi import get_asgi_application
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameBoosterss.settings')
 
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter , URLRouter
# from chat import routing as chatRouting
# from accounts import routing as orderRouting

def get_websocket_urlpatterns():
    # Import the routing modules here
    from chat import routing as chatRouting
    from accounts import routing as orderRouting
    
    # Combine the websocket_urlpatterns from both modules
    return chatRouting.websocket_urlpatterns + orderRouting.websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http" : get_asgi_application() ,
        "websocket" : AuthMiddlewareStack(
            URLRouter(
                get_websocket_urlpatterns()
            )   
        )
    }
)