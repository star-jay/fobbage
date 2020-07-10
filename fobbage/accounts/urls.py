from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    url(r'^simple_token/$',
        obtain_auth_token,
        name='simple-token'),
]
