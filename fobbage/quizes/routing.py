# # from django.conf.urls import url

# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack

# application = ProtocolTypeRouter({

#     # WebSocket chat handler
#     "websocket": AuthMiddlewareStack(
#         URLRouter([
#             # url(r"^chat/admin/$", AdminChatConsumer),
#             # url(r"^chat/$", PublicChatConsumer),
#         ])
#     ),
# })

# chat/routing.py
from django.conf.urls import url
from . import consumers

websocket_urlpatterns = [
    url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
]
