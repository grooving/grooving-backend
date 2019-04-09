from django.contrib.auth.models import User
from rest_framework import serializers
from Grooving.models import Artist, Portfolio
from user.serializers import UserSerializer
from portfolio.serializers import ArtisticGenderSerializer
from django.contrib.auth.hashers import make_password
from user.serializers import UserRegisterSerializer
from utils.Assertions import Assertions
from utils.notifications.notifications import Notifications


class ArtistInfoSerializer(serializers.HyperlinkedModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        depth = 1
        model = Artist
        fields = ('id', 'user', 'photo', 'phone', 'iban', 'paypalAccount')


class ShortPortfolioSerializer(serializers.ModelSerializer):
    artisticGender = ArtisticGenderSerializer(read_only=True, many=True)
    class Meta:

        model = Portfolio
        fields = ('id', 'artisticName', 'artisticGender')
        search_fields = ['artisticName', 'artisticGender__name']


class ListArtistSerializer(serializers.HyperlinkedModelSerializer):

    portfolio = ShortPortfolioSerializer(read_only=True)

    class Meta:
        model = Artist
        depth = 1
        fields = ('id', 'photo', 'rating', 'portfolio')


class ArtistSerializer(serializers.ModelSerializer):
    artisticName = serializers.CharField()

    class Meta:
        depth = 2
        model = Artist
        user = UserRegisterSerializer()
        fields = ('user', 'artisticName', 'phone', 'photo',)

    def save(self):

        artist = self._service_create_artist(self.initial_data)
        Notifications.send_email_welcome(artist.user.id)
        return artist

    def update(self, pk):

        artist = self._service_update_artist(self.initial_data, pk)
        return artist

    @staticmethod
    def _service_update_artist(json: dict, pk):

        artist = Artist.objects.get(pk=pk)
        artist.phone = json.get('phone')
        user = artist.user
        user_names = User.objects.values_list('username', flat=True)
        if json.get('username') != user.username:
            Assertions.assert_true_raise400('username' not in user_names,
                                            {"codeError": "Username already in the system"})
        user.first_name = json.get('first_name')
        Assertions.assert_true_raise400(user.first_name, {"codeError": "First name can't be null"})
        user.last_name = json.get('last_name')
        Assertions.assert_true_raise400(user.last_name, {"codeError": "Last name can't be null"})

        user.save()
        artist.user = user
        return artist

    @staticmethod
    def _service_create_artist(json: dict):

        user = User.objects.create(username=json.get('username'), password=make_password(json.get('password')),
                                   first_name=json.get('first_name'), last_name=json.get('last_name'),
                                   email=json.get('email'))

        portfolio1 = Portfolio.objects.create(artisticName=json.get('artisticName'))

        artist = Artist.objects.create(photo=json.get('photo'), phone=json.get('phone'),
                                       portfolio=portfolio1, user=user)

        return artist

    @staticmethod
    def validate_artist(request):

        user_names = User.objects.values_list('username', flat=True)
        emails = User.objects.values_list('email', flat=True)
        password = request.data.get("password")
        username = request.data.get("username")
        confirm_password = request.data.get("confirm_password")
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
        Assertions.assert_true_raise400(not(email in emails), {'error': "Email already in use"})

        # Password validations
        Assertions.assert_true_raise400(not(username in password or password in username),
                                        {'error': "Password can't be similar to the username"})

        Assertions.assert_true_raise400(not (email in password or password in username),
                                        {'error': "Password can't be similar to the email"})

        Assertions.assert_true_raise400(not (first_name in password or password in first_name),
                                        {'error': "Password can't be similar to the first name"})

        Assertions.assert_true_raise400(not (last_name in password or password in last_name),
                                        {'error': "Password can't be similar to the last name"})

        Assertions.assert_true_raise400('123' not in password and 'qwerty' not in password and
                                        not password.isnumeric(), {'error':  "Password must be complex"})

        Assertions.assert_true_raise400(len(password) > 7, {'error': "Password is too short"})

        Assertions.assert_true_raise400(username not in user_names, {'error': "Username already in use"})

        if phone:
            Assertions.assert_true_raise400(phone.isnumeric(), {'error': "Phone must be a number"})
            Assertions.assert_true_raise400(len(phone) == 9, {'error': "Phone length must be 9 digits"})

        Assertions.assert_true_raise400(len(first_name) > 1 and len(last_name) > 1,
                                        {'error': "First or second name do not seem real"})
        Assertions.assert_true_raise400('@' in email and '.' in email, {'error': "Invalid email"})
        return True

