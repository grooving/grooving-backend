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
    def _service_create_customer(json: dict):
        user1 = User.objects.create(username=json.get('username'),
                                    password=make_password(json.get('password')),
                                    first_name=json.get('first_name'),
                                    last_name=json.get('last_name'),
                                    email=json.get('email'))

        customer = Customer.objects.create(photo=json.get('photo'),phone = json.get('phone'),user = user1)
        customer.save()

        return customer

    @staticmethod
    def validate_customer(request):

        user_names = User.objects.values_list('username', flat=True)
        emails = User.objects.values_list('email', flat=True)
        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")
        username = request.data.get("username")
        email = request.data.get("email")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        phone = request.data.get("phone")

        Assertions.assert_true_raise400(request.data, {'error': "Empty form is not valid"})

        # Empty validations
        Assertions.assert_true_raise400(username, {'error': "Username field not provided"})
        Assertions.assert_true_raise400(password, {'error': "Password field not provided"})
        Assertions.assert_true_raise400(email, {'error': "Email field not provided"})
        Assertions.assert_true_raise400(first_name, {'error': "First name not provided"})
        Assertions.assert_true_raise400(last_name, {'error': "Last name not provided"})
        Assertions.assert_true_raise400(password == confirm_password, {'error': "Password and confirmation must match"})

        # Email in use validation
        Assertions.assert_true_raise400(not email in emails, {'error': "Email already in use"})

        # Password validations
        Assertions.assert_true_raise400(not (username in password or password in username),
                                        {'error': "Password can't be similar to the username"})

        Assertions.assert_true_raise400(not (email in password or password in username),
                                        {'error': "Password can't be similar to the email"})

        Assertions.assert_true_raise400(not (first_name in password or password in first_name),
                                        {'error': "Password can't be similar to the first name"})

        Assertions.assert_true_raise400(not (last_name in password or password in last_name),
                                        {'error': "Password can't be similar to the last name"})

        Assertions.assert_true_raise400('123' not in password and 'qwerty' not in password and
                                        not password.isnumeric(), {'error': "Password must be complex"})

        Assertions.assert_true_raise400(len(password) > 7, {'error': "Password is too short"})

        Assertions.assert_true_raise400(username not in user_names, {'error': "Username already in use"})

        if phone:
            Assertions.assert_true_raise400(phone.isnumeric(), "Phone must be a number")
            Assertions.assert_true_raise400(len(phone) == 9, "Phone length must be 9 digits")

        Assertions.assert_true_raise400(len(first_name) > 1 and len(last_name) > 1,
                                        "First or second name do not seem real")
        Assertions.assert_true_raise400('@' in email and '.' in email, "Invalid email")

        return True
