from django.conf.urls import url
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import UserInfoAPIView


urlpatterns = [
    url(r'user_info', UserInfoAPIView.as_view(), name='user_info'),
    url(r'^simple_token/$',
        obtain_auth_token,
        name='simple-token'),
]
