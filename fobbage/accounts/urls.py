from django.conf.urls import url
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    url(r'^simple_token/$',
        obtain_auth_token,
        name='simple-token'),
]
