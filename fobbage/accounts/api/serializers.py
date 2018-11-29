from django.contrib.auth import get_user_model
from rest_framework import serializers

# Get the UserModel
UserModel = get_user_model()


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        fields = ('pk', 'email', 'first_name', 'last_name',
                  'permissions')
        read_only_fields = ('email', )

    def get_permissions(self, user):
        return user.get_all_permissions()
