from django.conf.urls import url
from rest_framework_jwt.views import RefreshJSONWebToken
from .views import AuditedObtainJSONWebToken

urlpatterns = [

    url(r'^token/$',
        AuditedObtainJSONWebToken.as_view(),
        name='token'),

    url(r'^refreshtoken/$',
        RefreshJSONWebToken.as_view(),
        name='refreshtoken'),
]
