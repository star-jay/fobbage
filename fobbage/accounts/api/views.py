from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from rest_framework_jwt.views import ObtainJSONWebToken

from . import serializers

User = get_user_model()


class AuditedObtainJSONWebToken(ObtainJSONWebToken):
    """
    Wrapper around `ObtainJSONWebToken` that sends an audit signal
    when a user requests a token.
    """
    pass

# class UserRegistrationAPIView(generics.CreateAPIView):
#     """
#     Endpoint for user registration.
#     """

#     permission_classes = (permissions.AllowAny, )
#     serializer_class = serializers.UserRegistrationSerializer
#     queryset = User.objects.all()


# class UserEmailVerificationAPIView(views.APIView):
#     """
#     Endpoint for verifying email address.
#     """

#     permission_classes = (permissions.AllowAny, )

#     def get(self, request, verification_key):
#         activated_user = self.activate(verification_key)
#         if activated_user:
#             return Response(status=status.HTTP_200_OK)
#         return Response(status=status.HTTP_400_BAD_REQUEST)

#     def activate(self, verification_key):
#         return User.objects.activate_user(verification_key)


# class PasswordResetAPIView(views.APIView):
#     """
#     Endpoint to send email to user with password reset link.
#     """

#     permission_classes = (permissions.AllowAny, )
#     serializer_class = serializers.PasswordResetSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             try:
#                 user = User.objects.get(email=serializer.data['email'])
#                 user.send_password_reset_email(
#                     hostname=serializer.data['hostname'])
#             except User.DoesNotExist:
#                 pass
#             return Response(status=status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PasswordResetConfirmView(views.APIView):
#     """
#     Endpoint to change user password.
#     """

#     permission_classes = (permissions.AllowAny, )
#     serializer_class = serializers.PasswordResetConfirmSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(
#             data=request.data,
#             context={
#                 'uidb64': kwargs['uidb64'],
#                 'token': kwargs['token']
#             })

#         if serializer.is_valid(raise_exception=True):
#             new_password = serializer.validated_data.get('new_password')
#             user = serializer.user
#             user.set_password(new_password)
#             user.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class AcceptTermsAPIView(generics.UpdateAPIView):
#     """
#     Endpoint to accept terms and conditions.
#     """
#     model = User
#     permission_classes = (permissions.IsAuthenticated,)

#     def get_object(self, queryset=None):
#         obj = self.request.user
#         return obj

#     def update(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         if 'approve' in self.request.data:
#             if self.request.data['approve'] is True:
#                 self.object.has_approved_terms = True
#                 self.object.save()
#                 audit_signal.send(
#                     sender=User,
#                     user=self.object, action="APPROVE_TC")
#                 return Response("Success.", status=status.HTTP_200_OK)
#         return Response(
#             {'error': 'Must explicitly approve'},
#             status=status.HTTP_400_BAD_REQUEST
#         )


# class SettingsView(views.APIView):
#     """
#     Endpoint to patch specific settings
#     given settings are overwritten, other settings are left as is
#     """
#     # custom API views cannot use djangomodel permissions
#     permission_classes = (permissions.IsAuthenticated, HasAcceptedTerms)

#     def get(self, request, format=None):
#         user = request.user

#         serializer = serializers.EditSettingsSerializer(
#             data={'settings': user.settings},
#         )
#         if serializer.is_valid(raise_exception=True):
#             return Response(serializer.data, status=status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, *args, **kwargs):
#         serializer = serializers.EditSettingsSerializer(
#             data=request.data,
#         )

#         if serializer.is_valid(raise_exception=True):
#             user = request.user
#             for setting in serializer.data['settings']:
#                 user.settings[setting] = serializer.data['settings'][setting]

#             user.save()
#             return Response(user.settings, status=status.HTTP_200_OK)


# class PasswordChangeView(generics.UpdateAPIView):
#     """
#     An endpoint for changing password.
#     """
#     serializer_class = serializers.PasswordChangeSerializer
#     model = User
#     permission_classes = (permissions.IsAuthenticated,)

#     def get_object(self, queryset=None):
#         obj = self.request.user
#         return obj

#     def update(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         serializer = self.get_serializer(data=request.data)

#         if serializer.is_valid():
#             # Check old password
#             if not self.object.check_password(
#                 serializer.data.get("old_password")
#             ):
#                 return Response(
#                     {"old_password": ["Wrong password."]},
#                     status=status.HTTP_400_BAD_REQUEST)
#             # set_password also hashes the password that the user will get
#             self.object.set_password(serializer.data.get("new_password"))
#             self.object.save()
#             return Response("Success.", status=status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
