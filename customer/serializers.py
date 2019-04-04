from django.contrib.auth.models import User, Group
from rest_framework import serializers
from Grooving.models import Customer
from user.serializers import UserSerializer, ShortUserSerializer
from eventLocation.serializers import EventLocationSerializer, ShortEventLocationSerializer
from django.contrib.auth.hashers import make_password
from user.serializers import UserRegisterSerializer
from utils.Assertions import Assertions


class CustomerInfoSerializer(serializers.HyperlinkedModelSerializer):

    user = UserSerializer(read_only=True)
    eventLocations = EventLocationSerializer(read_only=True, many=True)

    class Meta:
        depth = 1
        model = Customer
        fields = ('id', 'user', 'photo', 'phone', 'iban', 'paypalAccount', 'eventLocations')


class PublicCustomerInfoSerializer(serializers.ModelSerializer):

    user = ShortUserSerializer(read_only=True)
    eventLocations = ShortEventLocationSerializer(read_only=True, many=True)

    class Meta:
        depth = 1
        model = Customer
        fields = ('id', 'user', 'photo', 'eventLocations')


class CustomerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        depth = 2
        user = UserRegisterSerializer()
        model = Customer
        fields = ('user', 'phone', 'photo',)

    def save(self):

        customer = self._service_create_customer(self.initial_data)
        return customer

    def update(self, pk):
        customer = self._service_update_customer(self.initial_data, pk)
        return customer

    @staticmethod
    def _service_update_customer(json: dict, pk):

        customer = Customer.objects.get(pk=pk)
        customer.phone = json.get('phone')
        customer.photo = json.get('photo')
        user = customer.user

        user.first_name = json.get('first_name')
        Assertions.assert_true_raise400(user.first_name, {"First name can't be null"})
        user.last_name = json.get('last_name')
        Assertions.assert_true_raise400(user.last_name, {"Last name can't be null"})

        user.save()
        customer.user = user
        return customer

    @staticmethod
    def _service_create_customer(json: dict, customer: Customer):
        user1 = User.objects.create(username=json.get('username'),
                                    password=make_password(json.get('password')),
                                    first_name=json.get('first_name'),
                                    last_name=json.get('last_name'),
                                    email=json.get('email'))

        customer.user = user1
        customer.photo = json.get('photo')
        customer.phone = json.get('phone')
        customer.save()

        return customer

    def validate_customer(self, request):

        user_names = User.objects.values_list('username', flat=True)
        emails = User.objects.values_list('email', flat=True)
        password = request.data.get("password")
        username = request.data.get("username")
        email = request.data.get("email")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")

        if email in emails:
            raise serializers.ValidationError("Email already used in the system")
        if username in user_names:
            raise serializers.ValidationError("Username already used in the system")
        if username is None:
            raise serializers.ValidationError("Username field not provided")
        if password is None:
            raise serializers.ValidationError("Password field not provided")
        if password != request.data.get("confirm_password"):
            raise serializers.ValidationError("Password and confirmation must match")
        if email is None:
            raise serializers.ValidationError("Email field not provided")
        if first_name is None:
            raise serializers.ValidationError("First name field not provided")
        if last_name is None:
            raise serializers.ValidationError("Last name field not provided")

        if username in password or password in username:
            raise serializers.ValidationError("Password can't be similar than username")

        if email in password or password in username:
            raise serializers.ValidationError("Last name can't be similar than username")

        if first_name in password or password in first_name:
            raise serializers.ValidationError("First name can't be similar than username")

        if last_name in password or password in last_name:
            raise serializers.ValidationError("Last name can't be similar than username")

        if len(password) < 8:
            raise serializers.ValidationError("Password length is too short")
        return True