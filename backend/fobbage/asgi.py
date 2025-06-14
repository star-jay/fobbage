"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""
import os
from django.core.asgi import get_asgi_application
from django.urls import re_path

# Load the ASGI APP before importing other APPS
# some weird channels order bug
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fobbage.settings")
application = get_asgi_application()
