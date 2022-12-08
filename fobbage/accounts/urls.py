from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import UserAPIView

urlpatterns = [
    path(r'user_info/', UserAPIView.as_view(), name='user-info'),
    path(r'simple_token/', obtain_auth_token, name='simple-token'),
]
