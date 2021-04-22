from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token

from .views import UserAPIView

urlpatterns = [
    url(r'user_info/$', UserAPIView.as_view(), name='user-info'),
    url(r'^simple_token/$',
        obtain_auth_token,
        name='simple-token'),
]
