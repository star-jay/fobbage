"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""
import os
from django.core.asgi import get_asgi_application
from django.urls import re_path
from channels.routing import (
    ProtocolTypeRouter, URLRouter)

# Load the ASGI APP before importing other APPS
# some weird channels order bug
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fobbage.settings")
django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack  # noqa: E402
from fobbage.quizes import consumers  # noqa: E402

# There is no longer a need for routing.py
# Routing is done here
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter([
            re_path(
                r'^ws/session/(?P<session_id>[^/]+)/$',
                consumers.ChatConsumer.as_asgi()),
        ])
    )
})
