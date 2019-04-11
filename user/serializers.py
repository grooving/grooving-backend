from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        depth = 1
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


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
