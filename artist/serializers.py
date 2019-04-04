from django.contrib.auth.models import User, Group
from rest_framework import serializers
from Grooving.models import Artist, Portfolio
from user.serializers import UserSerializer
from portfolio.serializers import ArtisticGenderSerializer
from django.contrib.auth.hashers import make_password
from user.serializers import UserRegisterSerializer


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
        fields = ('id', 'photo', 'portfolio')


class ArtistSerializer(serializers.ModelSerializer):
    artisticName = serializers.CharField()

    class Meta:
        depth = 2
        model = Artist
        user = UserRegisterSerializer()
        fields = ('user','artisticName', 'phone', 'photo',)

    def save(self):
        artist = Artist()
        artist = self._service_create_artist(self.initial_data, artist)
        return artist

    def update(self, pk):
        artist = Artist()
        artist = self._service_update_artist(self.initial_data,artist,pk)
        return artist

    @staticmethod
    def _service_update_artist(json: dict, artist: Artist,pk):

        artist = Artist.objects.get(pk=pk)
        artist.phone = json.get('phone')
        artist.photo = json.get('photo')
        artist.user.email = json.get('email')
        user = artist.user
        user.username = json.get('username')
        user.first_name = json.get('first_name')
        user.last_name = json.get('last_name')
        user.save()
        artist.user = user
        return artist
    @staticmethod
    def _service_create_artist(json: dict, artist: Artist):

        user = User.objects.create(username =json.get('username'),
                                   password=make_password(json.get('password')), first_name=json.get('first_name'),
                                   last_name=json.get('last_name'), email=json.get('email'))

        portfolio1 = Portfolio.objects.create(artisticName=json.get('artisticName'))


        artist = Artist.objects.create(photo='photo',phone='phone',portfolio=portfolio1,user=user)

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
        fields = ('id', 'rating', 'photo', 'portfolio')
