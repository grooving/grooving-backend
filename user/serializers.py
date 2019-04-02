from django.contrib.auth.models import User
from Grooving.models import Artist, Customer, Portfolio
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        depth = 1
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

class UserRegisterSerializer(serializers.HyperlinkedModelSerializer):
    confirm_password = serializers.CharField()

    class Meta:
        depth = 1
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'phone', 'photo', 'password','confirm_password')


class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    artisticName = serializers.CharField()
    class Meta:
        depth = 2
        model = Artist
        user = UserRegisterSerializer()
        fields = ('artisticName', 'user')

    def save(self):
        artist = Artist()
        artist = self._service_create_artist(self.initial_data, artist)
        return artist

    @staticmethod
    def _service_create_artist(json: dict, artist: Artist):

        user = User.objects.create(username =json.get('username'),
                                   password=make_password(json.get('password')), first_name=json.get('first_name'),
                                   last_name=json.get('last_name'), email=json.get('email'))

        portfolio1 = Portfolio.objects.create(artisticName=json.get('artisticName'))
        artist.user = user

        artist.photo = json.get('photo')
        artist.phone = json.get('phone')
        artist.portfolio = portfolio1
        artist.save()
        return artist

    def validate_artist(self, request):

        user_names = User.objects.values_list('username', flat=True)

        password = request.data.get("password")
        username = request.data.get("username")

        email = request.data.get("email")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")

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

class CustomerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        depth = 2
        user = UserRegisterSerializer()
        model = Customer
        fields = ('user',)

    def save(self):
        customer = Customer()
        customer = self._service_create_customer(self.initial_data, customer)
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
        password = request.data.get("password")
        username = request.data.get("username")
        email = request.data.get("email")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")

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