from django.contrib.auth import get_user_model
from rest_framework.decorators import action

from rest_framework import permissions, generics, response
from rest_framework.generics import mixins
from fobbage.accounts.serializers import UserSerializer, UserDetailsSerializer


User = get_user_model()


class UserAPIView(generics.ListCreateAPIView):
    # http_method_names = ['get', 'post', 'head', 'options']
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return response.Response(UserDetailsSerializer(request.user).data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @action(detail=True, methods=['post'], url_path="new_password")
    def set_password(self, request, pk=None):
        return self.update(request, pk=pk)
