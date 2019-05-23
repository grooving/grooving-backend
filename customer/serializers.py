from django.contrib.auth.models import User
from rest_framework import serializers
from Grooving.models import Customer
from user.serializers import UserSerializer, ShortUserSerializer
from eventLocation.serializers import EventLocationSerializer, ShortEventLocationSerializer
from django.contrib.auth.hashers import make_password
from user.serializers import UserRegisterSerializer
from utils.Assertions import Assertions
from utils.notifications.notifications import Notifications
from utils.strings import Strings
from customer.internationalization import translate
from utils.utils import check_accept_language, check_special_characters_and_numbers, check_is_number


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

    def save(self,request):

        customer = self._service_create_customer(self.initial_data,request)
        Notifications.send_email_welcome(customer.user.id)
        return customer

    def update(self, request, pk):
        customer = self._service_update_customer(self.initial_data, request, pk)
        return customer

    @staticmethod
    def _service_update_customer(json: dict, request, pk):
        language = check_accept_language(request)

        Assertions.assert_true_raise400(json, translate(language, "ERROR_EMPTY_JSON"))

        customer = Customer.objects.get(pk=pk)
        customer.phone = json.get('phone')

        user = customer.user

        user.email = json.get('email')
        password = json.get('password')

        first_name = request.data.get("first_name").strip()
        last_name = request.data.get("last_name").strip()
        email = request.data.get("email")
        username = request.data.get("username")
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

        user.first_name = json.get('first_name').strip()
        user.last_name = json.get('last_name').strip()

        customer.photo = json.get('photo')

        customer.paypalAccount = json.get('paypalAccount')

        if customer.paypalAccount:
            Assertions.assert_true_raise400('@' in customer.paypalAccount and '.' in customer.paypalAccount,
                                            translate(language, "ERROR_INVALID_PAYPAL_ACCOUNT"))

        user_in_db = User.objects.filter(email=user.email).first()
        if user_in_db:
            if user_in_db != user:
                if json.get('email') == user_in_db.email:
                    Assertions.assert_true_raise400(False, translate(language, "ERROR_EMAIL_IN_USE"))
        user.save()
        customer.user = user
        return customer

    @staticmethod
    def _service_create_customer(json: dict, request):

        language = check_accept_language(request)
        username = json.get('username')
        user_names = User.objects.values_list('username', flat=True)
        Assertions.assert_true_raise400(username not in user_names, translate(language, "ERROR_USERNAME_IN_USE"))
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

        user1 = User.objects.create(username=json.get('username'),
                                    password=make_password(json.get('password')),
                                    first_name=json.get('first_name'),
                                    last_name=json.get('last_name'),
                                    email=json.get('email'))

        customer = Customer.objects.create(photo=json.get('photo'), phone=json.get('phone'), user=user1)
        customer.save()

        return customer

    @staticmethod
    def validate_customer(request):
        language = check_accept_language(request)

        # Empty validations

        Assertions.assert_true_raise400(request.data, translate(language, "ERROR_EMPTY_FORM"))
        Assertions.assert_true_raise400(not check_is_number(request.data.get('username')),
                                        translate(language, "ERROR_USERNAME_CANT_BE_INTEGER"))
        Assertions.assert_true_raise400(request.data.get("username"), translate(language, "ERROR_EMPTY_USERNAME"))
        Assertions.assert_true_raise400(not check_is_number(request.data.get('email')),
                                        translate(language, "ERROR_EMAIL_CANT_BE_INTEGER"))
        Assertions.assert_true_raise400(request.data.get("email"), translate(language, "ERROR_EMAIL_MANDATORY"))
        Assertions.assert_true_raise400(Strings.check_max_length(request.data.get("username"), 30), translate(language, "ERROR_USERNAME_TOO_LONG"))
        Assertions.assert_true_raise400(Strings.check_max_length(request.data.get("email"), 50), translate(language, "ERROR_EMPTY_EMAIL"))
        Assertions.assert_true_raise400(request.data.get("first_name"), translate(language, "ERROR_EMPTY_FIRST_NAME"))
        Assertions.assert_true_raise400(request.data.get("last_name"), translate(language, "ERROR_EMPTY_LAST_NAME"))
        Assertions.assert_true_raise400(check_special_characters_and_numbers(request.data.get("first_name")),
                                        translate(language, "ERROR_FIRST_NAME_SPECIAL_CHARACTERS"))
        Assertions.assert_true_raise400(check_special_characters_and_numbers(request.data.get("last_name")),
                                        translate(language, "ERROR_LAST_NAME_SPECIAL_CHARACTERS"))

        username = request.data.get("username").strip()
        email = request.data.get("email")

        paypalAccount = request.data.get("paypalAccount")
        first_name = request.data.get("first_name").strip()
        last_name = request.data.get("last_name").strip()
        phone = request.data.get("phone")

        Assertions.assert_true_raise400(not check_is_number(request.data.get('photo')),
                                        translate(language, "ERROR_PHOTO_CANT_BE_INTEGER"))

        Assertions.assert_true_raise400(Strings.check_max_length(request.data.get('photo'), 500),
                                        translate(language, "ERROR_URL_TOO_LONG"))

        photo = request.data.get("photo")

        Assertions.assert_true_raise400(not check_is_number(request.data.get('paypalAccount')),
                                        translate(language, "ERROR_PAYPAL_CANT_BE_INTEGER"))
        if paypalAccount is not None:
            Assertions.assert_true_raise400('@' in paypalAccount and '.' in paypalAccount,
                                            translate(language, "ERROR_PAYPAL_EMAIL_INVALID"))

        if phone:
            try:
                Assertions.assert_true_raise400(phone.isnumeric(), translate(language, "ERROR_PHONE_MUST_BE_NUMBER"))
            except:
                Assertions.assert_true_raise400(False, translate(language, "ERROR_PHONE_MUST_BE_NUMBER"))
            Assertions.assert_true_raise400(len(phone) == 9, translate(language, "ERROR_PHONE_LENGTH_9"))

        Assertions.assert_true_raise400(not check_is_number(request.data.get('password')),
                                        translate(language, "ERROR_PASSWORD_CANT_BE_INTEGER"))
        Assertions.assert_true_raise400(request.data.get('password'),
                                        translate(language, "ERROR_PASSWORD_MANDATORY"))
        Assertions.assert_true_raise400(not check_is_number(request.data.get('confirm_password')),
                                        translate(language, "ERROR_CONFIRM_PASSWORD_CANT_BE_INTEGER"))
        Assertions.assert_true_raise400(request.data.get('confirm_password'),
                                        translate(language, "ERROR_CONFIRM_PASSWORD_MANDATORY"))
        Assertions.assert_true_raise400(Strings.check_max_length(request.data.get('first_name'), 30),
                                        translate(language, "ERROR_MAX_LENGTH_FIRST_NAME"))
        Assertions.assert_true_raise400(Strings.check_max_length(request.data.get('last_name'), 150),
                                        translate(language, "ERROR_MAX_LENGTH_LAST_NAME"))
        Assertions.assert_true_raise400(len(first_name) > 1, translate(language, "ERROR_FIRST_NAME_LENGTH"))
        Assertions.assert_true_raise400(len(last_name) > 1, translate(language, "ERROR_LAST_NAME_LENGTH"))
        Assertions.assert_true_raise400('@' in email and '.' in email, translate(language, "ERROR_EMAIL_INVALID"))
        Assertions.assert_true_raise400(len(email) > 5, translate(language, "ERROR_EMAIL_IS_TOO_SHORT"))



        if photo:
            Assertions.assert_true_raise400(photo.startswith(('http://', "https://")),
                                            translate(language, "ERROR_INVALID_PHOTO_URL_HTTP"))

        return True
