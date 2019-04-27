from django.contrib.auth.models import User
from rest_framework import serializers
from Grooving.models import Artist, Portfolio, Calendar
from user.serializers import UserSerializer
from portfolio.serializers import ArtisticGenderSerializer
from django.contrib.auth.hashers import make_password
from user.serializers import UserRegisterSerializer
from utils.Assertions import Assertions
from utils.strings import Strings
from utils.notifications.notifications import Notifications
from artist.internationalization import translate
from utils.utils import check_accept_language, check_special_characters_and_numbers


class EvenShorterPortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ('artisticName',)


class ArtistInfoSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)
    artisticName = EvenShorterPortfolioSerializer(read_only=True, source='portfolio')

    class Meta:
        depth = 1
        model = Artist
        fields = ('id', 'artisticName', 'user', 'photo', 'phone', 'iban', 'paypalAccount')


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
        fields = ('user', 'artisticName', 'phone', 'photo', 'paypalAccount')

    def save(self, request):

        artist = self._service_create_artist(self.initial_data, request)
        Notifications.send_email_welcome(artist.user.id)
        return artist

    def update(self, request, pk):

        artist = self._service_update_artist(self.initial_data, request, pk)
        return artist

    @staticmethod
    def _service_create_artist(json: dict, request):
        language = check_accept_language(request)

        # Check artisticName

        Assertions.assert_true_raise400(json.get('artisticName'),
                                        translate(language, "ERROR_EMPTY_ARTISTIC_NAME"))

        Assertions.assert_true_raise400(len(json.get('artisticName')) > 0,
                                        translate(language, "ERROR_EMPTY_ARTISTIC_NAME"))

        if Portfolio.objects.filter(artisticName__iexact=json.get('artisticName')):
            Assertions.assert_true_raise400(False, translate(language, "ERROR_ARTISTIC_NAME_ALREADY_EXISTS"))

        user = User.objects.create(username=json.get('username'), password=make_password(json.get('password')),
                                   first_name=json.get('first_name'), last_name=json.get('last_name'),
                                   email=json.get('email'))

        artist = Artist.objects.create(photo=json.get('photo'), phone=json.get('phone'), user=user)

        portfolio1 = Portfolio.objects.create(artisticName=json.get('artisticName'), artist=artist)

        Calendar.objects.create(days=[], portfolio=portfolio1)

        return artist

    @staticmethod
    def _service_update_artist(json: dict, request, pk):
        language = check_accept_language(request)

        Assertions.assert_true_raise400(json, translate(language, "ERROR_EMPTY_JSON"))

        artist = Artist.objects.get(pk=pk)
        artist.phone = json.get('phone')
        user = artist.user

        Assertions.assert_true_raise400(json.get('first_name'), translate(language, "ERROR_EMPTY_FIRST_NAME"))
        Assertions.assert_true_raise400(json.get('last_name'), translate(language, "ERROR_EMPTY_LAST_NAME"))

        user.first_name = json.get('first_name').strip()
        user.last_name = json.get('last_name').strip()

        artist.paypalAccount = json.get('paypalAccount')

        if artist.paypalAccount:
            Assertions.assert_true_raise400('@' in artist.paypalAccount and '.' in artist.paypalAccount,
                                            translate(language, "ERROR_INVALID_PAYPAL_ACCOUNT"))
        photo = json.get('photo')
        Assertions.assert_true_raise400(user.first_name, translate(language, "ERROR_EMPTY_FIRST_NAME"))
        Assertions.assert_true_raise400(user.last_name, translate(language, "ERROR_EMPTY_LAST_NAME"))

        if artist.phone:
            Assertions.assert_true_raise400(artist.phone.isnumeric(), translate(language, "ERROR_PHONE_MUST_BE_NUMBER"))
            Assertions.assert_true_raise400(len(artist.phone) == 9, translate(language, "ERROR_PHONE_LENGTH_9"))

        Assertions.assert_true_raise400(len(user.first_name) > 1,
                                        translate(language, "ERROR_FIRST_NAME_LENGTH"))
        Assertions.assert_true_raise400(len(user.last_name) > 1,
                                        translate(language, "ERROR_LAST_NAME_LENGTH"))
        if photo:
            Assertions.assert_true_raise400(photo.startswith(('http://', "https://")),
                                            translate(language, "ERROR_INVALID_PHOTO_URL_HTTP"))
            Assertions.assert_true_raise400(Strings.url_is_an_image(photo),
                                            translate(language, "ERROR_INVALID_PHOTO_URL_ENDFORMAT"))

        artistic_name = json.get('artisticName')

        Assertions.assert_true_raise400(artistic_name, translate(language, "ERROR_NO_ARTISTIC_NAME"))
        Assertions.assert_true_raise400(artistic_name != "", translate(language, "ERROR_NO_ARTISTIC_NAME"))

        # Comprobación: el artisticName nuevo (del request), no debe coincidir con ninguno del resto de artistas que no sea yo

        if Portfolio.objects.exclude(artist__id=artist.id).filter(artisticName__iexact=json.get('artisticName')):
            Assertions.assert_true_raise400(False, translate(language, "ERROR_ARTISTIC_NAME_ALREADY_EXISTS"))

        try:
            portfolio = Portfolio.objects.get(artist=artist)

            portfolio.artisticName = artistic_name
            user.save()

            artist.user = user

            portfolio.save()

            return artist
        except Portfolio.DoesNotExist:
            Assertions.assert_true_raise400(False, translate(language, "ERROR_NOTFOUND_PORTFOLIO"))

    @staticmethod
    def validate_artist(request):
        language = check_accept_language(request)

        # Empty validations

        Assertions.assert_true_raise400(request.data, translate(language, "ERROR_EMPTY_FORM"))
        Assertions.assert_true_raise400(request.data.get("username"), translate(language, "ERROR_EMPTY_USERNAME"))
        Assertions.assert_true_raise400(request.data.get("password"), translate(language, "ERROR_EMPTY_PASSWORD"))
        Assertions.assert_true_raise400(request.data.get("confirm_password"),
                                        translate(language, "ERROR_EMPTY_CONFIRM_PASSWORD"))
        Assertions.assert_true_raise400(
            request.data.get("password").strip() == request.data.get("confirm_password").strip(),
            translate(language, "ERROR_PASSWORD_&_CONFIRM_MUST_BE_EQUALS"))
        Assertions.assert_true_raise400(request.data.get("email"), translate(language, "ERROR_EMPTY_EMAIL"))
        Assertions.assert_true_raise400(request.data.get("first_name"), translate(language, "ERROR_EMPTY_FIRST_NAME"))
        Assertions.assert_true_raise400(request.data.get("last_name"), translate(language, "ERROR_EMPTY_LAST_NAME"))
        Assertions.assert_true_raise400(check_special_characters_and_numbers(request.data.get("first_name")),
                                        translate(language, "ERROR_FIRST_NAME_SPECIAL_CHARACTERS"))
        Assertions.assert_true_raise400(check_special_characters_and_numbers(request.data.get("last_name")),
                                        translate(language, "ERROR_LAST_NAME_SPECIAL_CHARACTERS"))

        username = request.data.get("username").strip()
        password = request.data.get("password").strip()
        email = request.data.get("email").strip()
        first_name = request.data.get("first_name").strip()
        last_name = request.data.get("last_name").strip()

        user_names = User.objects.values_list('username', flat=True)
        emails = User.objects.values_list('email', flat=True)

        phone = request.data.get("phone")
        photo = request.data.get("photo")

        # Email in use validation

        Assertions.assert_true_raise400(not (email in emails), translate(language, "ERROR_EMAIL_IN_USE"))

        # Password validations

        Assertions.assert_true_raise400(not (username in password or password in username),
                                        translate(language, "ERROR_PASSWORD_SIMILAR_USERNAME"))

        Assertions.assert_true_raise400(not (email in password or password in email),
                                        translate(language, "ERROR_PASSWORD_SIMILAR_EMAIL"))

        Assertions.assert_true_raise400(not (first_name in password or password in first_name),
                                        translate(language, "ERROR_PASSWORD_SIMILAR_FIRST_NAME"))

        Assertions.assert_true_raise400(not (last_name in password or password in last_name),
                                        translate(language, "ERROR_PASSWORD_SIMILAR_LAST_NAME"))

        Assertions.assert_true_raise400('123' not in password and 'qwerty' not in password and
                                        not password.isnumeric(), translate(language, "ERROR_PASSWORD_MUST_BE_COMPLEX"))

        Assertions.assert_true_raise400(len(password) > 7, translate(language, "ERROR_PASSWORD_IS_TOO_SHORT"))

        Assertions.assert_true_raise400(username not in user_names, translate(language, "ERROR_USERNAME_IN_USE"))

        if phone:
            Assertions.assert_true_raise400(phone.isnumeric(), translate(language, "ERROR_PHONE_MUST_BE_NUMBER"))
            Assertions.assert_true_raise400(len(phone) == 9, translate(language, "ERROR_PHONE_LENGTH_9"))

        Assertions.assert_true_raise400(len(first_name) > 1, translate(language, "ERROR_FIRST_NAME_LENGTH"))
        Assertions.assert_true_raise400(len(last_name) > 1, translate(language, "ERROR_LAST_NAME_LENGTH"))

        Assertions.assert_true_raise400(len(email) > 5, translate(language, "ERROR_EMAIL_IS_TOO_SHORT"))
        Assertions.assert_true_raise400('@' in email and '.' in email, translate(language, "ERROR_EMAIL_INVALID"))

        if photo:
            Assertions.assert_true_raise400(photo.startswith(('http://', "https://")),
                                            translate(language, "ERROR_INVALID_PHOTO_URL_HTTP"))
            Assertions.assert_true_raise400(Strings.url_is_an_image(photo),
                                            translate(language, "ERROR_INVALID_PHOTO_URL_ENDFORMAT"))
            return True
