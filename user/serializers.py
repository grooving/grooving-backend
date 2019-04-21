from Grooving.models import Admin, Artist, Customer, Portfolio
from django.contrib.auth.models import User
from rest_framework import serializers
from utils.Assertions import Assertions
from eventLocation.serializers import ShortEventLocationSerializer
from portfolio.serializers import ArtisticGenderSerializer


class ShortPortfolioSerializer(serializers.ModelSerializer):
    artisticGender = ArtisticGenderSerializer(read_only=True, many=True)
    class Meta:

        model = Portfolio
        fields = ('id', 'artisticName', 'artisticGender')
        search_fields = ['artisticName', 'artisticGender__name']


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        depth = 1
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'is_active')

    @staticmethod
    def validate_ban_user(attrs):

        # Admin validation

        admin = Admin.objects.filter(user=attrs.user).first()
        Assertions.assert_true_raise403(admin is not None, {'error': 'ERROR_USER_FORBIDDEN'})

        # Data validation

        json = attrs.data
        Assertions.assert_true_raise400(json.get('id'), {'error': 'ERROR_FIELD_ID'})

        # Ban user validation

        user = User.objects.filter(id=json.get('id')).first()
        Assertions.assert_true_raise400(user is not None, {'error': 'ERROR_BAN_USER_UNKNOWN'})

        return True


class ShortUserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        depth = 1
        model = User
        fields = ('first_name', 'last_name', 'username')


class UserSerializerForAdmin(serializers.HyperlinkedModelSerializer):

    class Meta:
        depth = 1
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'is_active')


class UserRegisterSerializer(serializers.HyperlinkedModelSerializer):
    confirm_password = serializers.CharField()

    class Meta:
        depth = 1
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'confirm_password', 'paypalAccount')


class ListArtistSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializerForAdmin(read_only=True)
    portfolio = ShortPortfolioSerializer(read_only=True)

    class Meta:
        model = Artist
        depth = 1
        fields = ('id', 'user', 'photo', 'portfolio')


class PublicCustomerInfoSerializer(serializers.ModelSerializer):

    user = UserSerializerForAdmin(read_only=True)
    eventLocations = ShortEventLocationSerializer(read_only=True, many=True)

    class Meta:
        depth = 1
        model = Customer
        fields = ('id', 'user', 'photo', 'eventLocations')
