from django.contrib.auth import get_user_model
from rest_framework import serializers

# Get the UserModel
UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = UserModel.objects.create(
            **validated_data
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = UserModel
        # Tuple of serialized model fields (see link [2])
        fields = (
            "id", "username", "email", "first_name", "last_name", "password", )


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
