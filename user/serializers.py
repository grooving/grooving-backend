from Grooving.models import Admin, Artist, Customer, Portfolio, Calendar, PortfolioModule, PaymentPackage, Offer, EventLocation, Zone
from django.contrib.auth.models import User
from rest_framework import serializers
from utils.Assertions import Assertions
from eventLocation.serializers import ShortEventLocationSerializer
from portfolio.serializers import ArtisticGenderSerializer
from utils.utils import check_accept_language
from .internationalization import translate


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

        language = check_accept_language(attrs)

        # Admin validation

        admin = Admin.objects.filter(user=attrs.user).first()
        Assertions.assert_true_raise403(admin is not None, translate(language, 'ERROR_USER_FORBIDDEN'))

        # Data validation

        json = attrs.data
        Assertions.assert_true_raise400(json.get('id') and str(json.get('id')).isdigit(), translate(language, 'ERROR_FIELD_ID'))

        # Ban user validation

        user = User.objects.filter(id=json.get('id')).first()
        Assertions.assert_true_raise400(user is not None, translate(language, 'ERROR_BAN_USER_UNKNOWN'))

        return True

    @staticmethod
    def anonymize_and_hide_artist(artist: Artist):
        portfolio = Portfolio.objects.filter(artist=artist).first()
        portfolio.isHidden = True
        portfolio.artisticName = None
        portfolio.banner = None
        portfolio.biography = None
        portfolio.save()

        PortfolioModule.objects.filter(portfolio=portfolio).delete()
        Calendar.objects.filter(portfolio=portfolio).update(days=[])

        for p in PaymentPackage.objects.filter(portfolio=portfolio):

            p.description = None
            p.save()
            if p.performance:
                p.performance.info = "****"
                p.performance.save()

            for o in Offer.objects.filter(paymentPackage=p):

                if o.chat:
                    o.chat.delete()
                if o.transaction:
                    o.transaction.paypalArtist = None
                    o.transaction.save()

    @staticmethod
    def anonymize_and_hide_customer(customer: Customer):
        for e in EventLocation.objects.filter(customer=customer):

            e.isHidden = True
            e.name = None
            e.address = "****"
            e.equipment = None
            e.description = None
            e.save()

            for o in Offer.objects.filter(eventLocation=e):

                if o.chat:
                    o.chat.delete()
                if o.rating:
                    o.rating.comment = None
                    o.rating.save()


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
