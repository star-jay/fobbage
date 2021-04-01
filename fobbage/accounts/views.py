from django.contrib.auth import get_user_model
from rest_framework.decorators import action

from rest_framework import permissions, viewsets
from fobbage.accounts.serializers import UserSerializer


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.for_user(self.request.user)

    @action(detail=True, methods=['post'], url_path="new_password")
    def set_password(self, request, pk=None):
        return self.update(request, pk=pk)
