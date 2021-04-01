from django.conf.urls import url
from django.urls import path, include
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter


from .views import UserViewSet


router = DefaultRouter()
router.register(r'user_info', UserViewSet, basename='user_info')

urlpatterns = [
    path('', include(router.urls)),
    url(r'^simple_token/$',
        obtain_auth_token,
        name='simple-token'),
]
