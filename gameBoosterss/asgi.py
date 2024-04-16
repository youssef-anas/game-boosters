import os
from django.core.asgi import get_asgi_application
import importlib

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameBoosterss.settings')
 
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter , URLRouter
# from chat import routing as chatRouting
# from accounts import routing as orderRouting

def get_websocket_urlpatterns():
    # Import the routing modules as strings
    chatRouting_module = importlib.import_module('chat.routing')
    orderRouting_module = importlib.import_module('accounts.routing')
    
    # Get the websocket_urlpatterns from both modules
    chat_websocket_urlpatterns = getattr(chatRouting_module, 'websocket_urlpatterns', [])
    order_websocket_urlpatterns = getattr(orderRouting_module, 'websocket_urlpatterns', [])
    
    # Combine the websocket_urlpatterns from both modules
    return chat_websocket_urlpatterns + order_websocket_urlpatterns

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