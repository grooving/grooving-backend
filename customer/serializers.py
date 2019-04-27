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
from utils.utils import check_accept_language


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
        customer.photo = json.get('photo')
        user = customer.user
        user.first_name = json.get('first_name').strip()
        user.last_name = json.get('last_name').strip()
        photo = json.get('photo')

        customer.paypalAccount = json.get('paypalAccount')

        if customer.paypalAccount:
            Assertions.assert_true_raise400('@' in customer.paypalAccount and '.' in customer.paypalAccount,
                                            translate(language, "ERROR_INVALID_PAYPAL_ACCOUNT"))

        Assertions.assert_true_raise400(user.first_name, translate(language, "ERROR_EMPTY_FIRST_NAME"))
        Assertions.assert_true_raise400(user.last_name, translate(language, "ERROR_EMPTY_LAST_NAME"))

        if customer.phone:
            Assertions.assert_true_raise400(customer.phone.isnumeric(),
                                            translate(language, "ERROR_PHONE_MUST_BE_NUMBER"))
            Assertions.assert_true_raise400(len(customer.phone) == 9, translate(language, "ERROR_PHONE_LENGTH_9"))

        Assertions.assert_true_raise400(len(user.first_name) > 1, translate(language, "ERROR_FIRST_NAME_LENGTH"))
        Assertions.assert_true_raise400(len(user.last_name) > 1, translate(language, "ERROR_LAST_NAME_LENGTH"))

        if photo:
            Assertions.assert_true_raise400(photo.startswith(('http://', "https://")),
                                            translate(language, "ERROR_INVALID_PHOTO_URL_HTTP"))
            Assertions.assert_true_raise400(Strings.url_is_an_image(photo),
                                            translate(language, "ERROR_INVALID_PHOTO_URL_ENDFORMAT"))

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

        customer = Customer.objects.create(photo=json.get('photo'), phone=json.get('phone'), user=user1)
        customer.save()

        return customer

    @staticmethod
    def validate_customer(request):
        language = check_accept_language(request)

        user_names = User.objects.values_list('username', flat=True)
        emails = User.objects.values_list('email', flat=True)
        password = request.data.get("password").strip()
        confirm_password = request.data.get("confirm_password").strip()
        username = request.data.get("username").strip()
        email = request.data.get("email")
        first_name = request.data.get("first_name").strip()
        last_name = request.data.get("last_name").strip()
        phone = request.data.get("phone")
        photo = request.data.get("photo")
        Assertions.assert_true_raise400(request.data, translate(language, "ERROR_EMPTY_FORM"))

        # Empty validations
        Assertions.assert_true_raise400(username, translate(language, "ERROR_EMPTY_USERNAME"))
        Assertions.assert_true_raise400(password, translate(language, "ERROR_EMPTY_PASSWORD"))
        Assertions.assert_true_raise400(email, translate(language, "ERROR_EMPTY_EMAIL"))
        Assertions.assert_true_raise400(first_name, translate(language, "ERROR_EMPTY_FIRST_NAME"))
        Assertions.assert_true_raise400(last_name, translate(language, "ERROR_EMPTY_LAST_NAME"))
        Assertions.assert_true_raise400(password == confirm_password,
                                        translate(language, "ERROR_PASSWORD_&_CONFIRM_MUST_BE_EQUALS"))

        # Email in use validation
        Assertions.assert_true_raise400(not (email in emails),
                                        translate(language, "ERROR_EMAIL_IN_USE"))

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
        Assertions.assert_true_raise400('@' in email and '.' in email, translate(language, "ERROR_EMAIL_INVALID"))
        Assertions.assert_true_raise400(len(email) > 5, translate(language, "ERROR_EMAIL_IS_TOO_SHORT"))

        if photo:
            Assertions.assert_true_raise400(photo.startswith(('http://', "https://")),
                                            translate(language, "ERROR_INVALID_PHOTO_URL_HTTP"))
            Assertions.assert_true_raise400(Strings.url_is_an_image(photo),
                                            translate(language, "ERROR_INVALID_PHOTO_URL_ENDFORMAT"))

        return True
