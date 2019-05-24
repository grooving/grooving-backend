from _json import make_encoder

from django.contrib.auth.models import User
from rest_framework import serializers
from Grooving.models import Artist, Portfolio, Calendar, ArtisticGender
from user.serializers import UserSerializer
from artistGender.serializers import ArtisticGenderSerializerOut
from django.contrib.auth.hashers import make_password
from user.serializers import UserRegisterSerializer
from utils.Assertions import Assertions
from utils.strings import Strings
from utils.notifications.notifications import Notifications
from artist.internationalization import translate
from cdn.views import register_profile_photo_upload
from utils.utils import check_accept_language, check_special_characters_and_numbers, check_is_number

from rest_framework.response import Response


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

    artisticGender = ArtisticGenderSerializerOut(read_only=True, many=True)


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
        email = json.get('email')
        emails = User.objects.values_list('email', flat=True)
        Assertions.assert_true_raise400(not (email in emails), translate(language, "ERROR_EMAIL_IN_USE"))

        Assertions.assert_true_raise400(request.data.get("password"), translate(language, "ERROR_EMPTY_PASSWORD"))
        Assertions.assert_true_raise400(request.data.get("confirm_password"),
                                        translate(language, "ERROR_EMPTY_CONFIRM_PASSWORD"))
        Assertions.assert_true_raise400(Strings.check_max_length(request.data.get("password"), 30),
                                        translate(language, "ERROR_PASSWORD_TOO_LONG"))

        Assertions.assert_true_raise400(
            request.data.get("password").strip() == request.data.get("confirm_password").strip(),
            translate(language, "ERROR_PASSWORD_&_CONFIRM_MUST_BE_EQUALS"))

        password = request.data.get('password')
        username = request.data.get('username')
        first_name = request.data.get("first_name").strip()
        last_name = request.data.get("last_name").strip()
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
        if Portfolio.objects.filter(artisticName__iexact=json.get('artisticName')):
            Assertions.assert_true_raise400(False, translate(language, "ERROR_ARTISTIC_NAME_ALREADY_EXISTS"))
        username = json.get('username')
        user_names = User.objects.values_list('username', flat=True)
        Assertions.assert_true_raise400(username not in user_names, translate(language, "ERROR_USERNAME_IN_USE"))

        user = User.objects.create(username=json.get('username'), password=make_password(json.get('password')),
                                   first_name=json.get('first_name'), last_name=json.get('last_name'),
                                   email=json.get('email'))

        Assertions.assert_true_raise400(Strings.check_max_length(request.data.get('artisticName'), 140),
                                        translate(language, "ERROR_ARTISTICNAME_TOO_LONG"))

        image64 = json.get('image64')
        ext = json.get('ext')

        artist = Artist.objects.create(phone=json.get('phone'), user=user)

        if image64 and ext:
            photo = register_profile_photo_upload(image64, ext, user)
            artist.photo = photo

        artist.save()
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

        user.first_name = json.get('first_name').strip()
        user.last_name = json.get('last_name').strip()
        # New 19/05

        user.email = json.get('email')

        first_name = request.data.get("first_name").strip()
        last_name = request.data.get("last_name").strip()
        email = request.data.get("email")
        username = request.data.get("username")
        password = json.get('password')
        if password:
            Assertions.assert_true_raise400(Strings.check_max_length(request.data.get("password"), 30),
                                            translate(language, "ERROR_PASSWORD_TOO_LONG"))

            Assertions.assert_true_raise400(
                request.data.get("password").strip() == request.data.get("confirm_password").strip(),
                translate(language, "ERROR_PASSWORD_&_CONFIRM_MUST_BE_EQUALS"))
            Assertions.assert_true_raise400(not (username in password or password in username),
                                            translate(language, "ERROR_PASSWORD_SIMILAR_USERNAME"))

            Assertions.assert_true_raise400(not (email in password or password in email),
                                            translate(language, "ERROR_PASSWORD_SIMILAR_EMAIL"))

            Assertions.assert_true_raise400(not (first_name in password or password in first_name),
                                            translate(language, "ERROR_PASSWORD_SIMILAR_FIRST_NAME"))

            Assertions.assert_true_raise400(not (last_name in password or password in last_name),
                                            translate(language, "ERROR_PASSWORD_SIMILAR_LAST_NAME"))

            Assertions.assert_true_raise400('123' not in password and 'qwerty' not in password and
                                            not password.isnumeric(),
                                            translate(language, "ERROR_PASSWORD_MUST_BE_COMPLEX"))

            Assertions.assert_true_raise400(len(password) > 7, translate(language, "ERROR_PASSWORD_IS_TOO_SHORT"))

            user.password = make_password(password)

        image64 = json.get('image64')
        ext = json.get('ext')
        if image64 and ext:
            photo = register_profile_photo_upload(image64, ext, user)
            artist.photo = photo

        #
        if json.get('paypalAccount'):
            Assertions.assert_true_raise400(Strings.check_max_length(json.get('paypalAccount'), 100),
                                        translate(language, "ERROR_PAYPAL_TOO_LONG"))

        artist.paypalAccount = json.get('paypalAccount')

        if artist.paypalAccount:
            Assertions.assert_true_raise400('@' in artist.paypalAccount and '.' in artist.paypalAccount,
                                            translate(language, "ERROR_INVALID_PAYPAL_ACCOUNT"))


        artistic_name = json.get('artisticName')

        Assertions.assert_true_raise400(artistic_name, translate(language, "ERROR_NO_ARTISTIC_NAME"))
        Assertions.assert_true_raise400(artistic_name != "", translate(language, "ERROR_NO_ARTISTIC_NAME"))

        # Comprobación: el artisticName nuevo (del request), no debe coincidir con ninguno del resto de artistas
        # que no sea yo

        if Portfolio.objects.exclude(artist__id=artist.id).filter(artisticName__iexact=json.get('artisticName')):
            Assertions.assert_true_raise400(False, translate(language, "ERROR_EMAIL_IN_USE"))

        user_in_db = User.objects.filter(email=user.email).first()
        if user_in_db:
            if user_in_db != user:
                if json.get('email') == user_in_db.email:
                    Assertions.assert_true_raise400(False, translate(language, "ERROR_EMAIL_IN_USE"))

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
        Assertions.assert_true_raise400(not check_is_number(request.data.get('username')),
                                        translate(language, "ERROR_USERNAME_CANT_BE_INTEGER"))
        Assertions.assert_true_raise400(request.data.get("username"), translate(language, "ERROR_EMPTY_USERNAME"))
        Assertions.assert_true_raise400(request.data.get("artisticName"),
                                        translate(language, "ERROR_ARTISTICNAME_MANDATORY"))
        Assertions.assert_true_raise400(not check_is_number(request.data.get("artisticName")),
                                        translate(language, "ERROR_ARTISTICNAME_CANT_BE_INTEGER"))
        Assertions.assert_true_raise400(not check_is_number(request.data.get('email')),
                                        translate(language, "ERROR_EMAIL_CANT_BE_INTEGER"))
        Assertions.assert_true_raise400(request.data.get("email"), translate(language, "ERROR_EMAIL_TOO_LONG"))
        Assertions.assert_true_raise400(Strings.check_max_length(request.data.get("username"), 30), translate(language, "ERROR_USERNAME_TOO_LONG"))
        Assertions.assert_true_raise400(Strings.check_max_length(request.data.get("email"), 50), translate(language, "ERROR_EMPTY_EMAIL"))
        Assertions.assert_true_raise400(request.data.get("first_name"), translate(language, "ERROR_EMPTY_FIRST_NAME"))
        Assertions.assert_true_raise400(request.data.get("last_name"), translate(language, "ERROR_EMPTY_LAST_NAME"))
        Assertions.assert_true_raise400(check_special_characters_and_numbers(request.data.get("first_name")),
                                        translate(language, "ERROR_FIRST_NAME_SPECIAL_CHARACTERS"))
        Assertions.assert_true_raise400(check_special_characters_and_numbers(request.data.get("last_name")),
                                        translate(language, "ERROR_LAST_NAME_SPECIAL_CHARACTERS"))

        Assertions.assert_true_raise400(Strings.check_max_length(request.data.get('first_name'), 30),
                                        translate(language, "ERROR_MAX_LENGTH_FIRST_NAME"))
        Assertions.assert_true_raise400(Strings.check_max_length(request.data.get('last_name'), 150),
                                        translate(language, "ERROR_MAX_LENGTH_LAST_NAME"))
        Assertions.assert_true_raise400(Strings.check_max_length(request.data.get('last_name'), 150),
                                        translate(language, "ERROR_MAX_LENGTH_LAST_NAME"))


        username = request.data.get("username").strip()
        email = request.data.get("email").strip()
        first_name = request.data.get("first_name").strip()
        last_name = request.data.get("last_name").strip()
        paypalAccount = request.data.get("paypalAccount")

        Assertions.assert_true_raise400(not check_is_number(request.data.get('paypalAccount')),
                                        translate(language, "ERROR_PAYPAL_CANT_BE_INTEGER"))
        if paypalAccount is not None:
            Assertions.assert_true_raise400('@' in paypalAccount and '.' in paypalAccount,
                                            translate(language, "ERROR_PAYPAL_EMAIL_INVALID"))
        phone = request.data.get("phone")
        photo = request.data.get("photo")

        if phone:
            try:
                Assertions.assert_true_raise400(phone.isnumeric(), translate(language, "ERROR_PHONE_MUST_BE_NUMBER"))
            except:
                Assertions.assert_true_raise400(False, translate(language, "ERROR_PHONE_MUST_BE_NUMBER"))
            Assertions.assert_true_raise400(len(phone) == 9, translate(language, "ERROR_PHONE_LENGTH_9"))

        Assertions.assert_true_raise400(not check_is_number(request.data.get('password')),
                                        translate(language, "ERROR_PASSWORD_CANT_BE_INTEGER"))
        Assertions.assert_true_raise400(not check_is_number(request.data.get('confirm_password')),
                                        translate(language, "ERROR_CONFIRM_PASSWORD_CANT_BE_INTEGER"))

        Assertions.assert_true_raise400(len(first_name) > 1, translate(language, "ERROR_FIRST_NAME_LENGTH"))
        Assertions.assert_true_raise400(len(last_name) > 1, translate(language, "ERROR_LAST_NAME_LENGTH"))

        Assertions.assert_true_raise400(len(email) > 5, translate(language, "ERROR_EMAIL_IS_TOO_SHORT"))
        Assertions.assert_true_raise400('@' in email and '.' in email, translate(language, "ERROR_EMAIL_INVALID"))

        return True
