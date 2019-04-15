from Grooving.models import Admin
from django.contrib.auth.models import User
from rest_framework import serializers
from utils.Assertions import Assertions


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        depth = 1
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'is_active')

    @staticmethod
    def validate_ban_user(attrs):

        # Admin validation

        admin = Admin.objects.filter(user=attrs.user).first()
        Assertions.assert_true_raise403(admin is not None, {'error': 'ERROR_USER_FORBIDDEN'})

        # Ban user validation

        json = attrs.data
        user = User.objects.filter(id=json.get('id')).first()
        Assertions.assert_true_raise400(user is not None, {'error': 'ERROR_USER_FORBIDDEN'})

        return True


class ShortUserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        depth = 1
        model = User
        fields = ('first_name', 'last_name', 'username')


class UserRegisterSerializer(serializers.HyperlinkedModelSerializer):
    confirm_password = serializers.CharField()

    class Meta:
        depth = 1
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'confirm_password', 'paypalAccount')
