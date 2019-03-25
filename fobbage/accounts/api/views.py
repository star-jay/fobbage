from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model # If used custom user model

from .serializers import UserSerializer

from .serializers import UserDetailsSerializer


User = get_user_model()


class AuditedObtainJSONWebToken(ObtainJSONWebToken):
    """
    Wrapper around `ObtainJSONWebToken` that sends an audit signal
    when a user requests a token.
    """
    pass


class CreateUserView(CreateAPIView):

    model = get_user_model()
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserSerializer