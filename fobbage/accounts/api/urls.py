from django.conf.urls import url
from rest_framework_jwt.views import RefreshJSONWebToken
from .views import AuditedObtainJSONWebToken

from . import views

urlpatterns = [

    url(r'^token/$',
        AuditedObtainJSONWebToken.as_view(),
        name='token'),

    # url(r'^refreshtoken/$',
    #     RefreshJSONWebToken.as_view(),
    #     name='refreshtoken'),

    # url(r'^registration/$',
    #     views.UserRegistrationAPIView.as_view(),
    #     name='userregistration'),

    # url(r'^emailverification/(?P<verification_key>.+)/$',
    #     views.UserEmailVerificationAPIView.as_view(),
    #     name='emailverification'),

    # url(r'^passwordreset/$',
    #     views.PasswordResetAPIView.as_view(),
    #     name='passwordreset'),

    # url(r'^passwordreset-confirmation/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',  # noqa: E501
    #     views.PasswordResetConfirmView.as_view(),
    #     name='passwordreset-confirmation'),

    # url(r'^accept-terms/$',
    #     views.AcceptTermsAPIView.as_view(),
    #     name='accept-terms'),

    # url(r'^settings/$',
    #     views.SettingsView.as_view(),
    #     name='settings'),

    # url(r'^passwordchange/$',
    #     views.PasswordChangeView.as_view(),
    #     name='passwordchange'),
]
