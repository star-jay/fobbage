# mysite/routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from fobbage.quizes.routing import websocket_urlpatterns
# from fobbage.quizes.consumers import EchoConsumer?

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
    # 'channel': ChannelNameRouter({
    #     "experiment-start": EchoConsumer,
    # }),
})
