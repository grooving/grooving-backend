from Grooving.models import Offer, Artist, Customer
from rest_framework import generics
from .serializers import ListArtistOffersSerializer, ListCustomerOffersSerializer
from utils.authentication_utils import get_user_type, get_logged_user
from utils.utils import auto_update_old_offers
from utils.Assertions import Assertions


class ListArtistOffers(generics.ListAPIView):

    serializer_class = ListArtistOffersSerializer

    def get_queryset(self):

        user = get_logged_user(self.request)
        user_type = get_user_type(user)

        Assertions.assert_true_raise403(user is not None, {'error': 'ERROR_NOT_LOGGED_IN'})
        Assertions.assert_true_raise403(user_type == 'Artist', {'error': 'ERROR_NOT_AN_ARTIST'})
        try:
            artist = Artist.objects.get(user_id=user.user_id)

            queryset = Offer.objects.filter(paymentPackage__portfolio__artist=artist)
            auto_update_old_offers(queryset)
            return queryset
        except Artist.DoesNotExist:
            booleano = False
            Assertions.assert_true_raise400(booleano, {'error': 'ERROR_NO_ARTIST_FOUND'})


class ListCustomerOffers(generics.ListAPIView):

    serializer_class = ListCustomerOffersSerializer

    def get_queryset(self):

        user = get_logged_user(self.request)
        user_type = get_user_type(user)
        Assertions.assert_true_raise403(user is not None, {'error': 'ERROR_NOT_LOGGED_IN'})
        Assertions.assert_true_raise403(user_type == 'Customer', {'error': 'ERROR_NOT_A_CUSTOMER'})
        try:
            customer = Customer.objects.get(user_id=user.user_id)
            queryset = Offer.objects.filter(eventLocation__customer=customer)
            auto_update_old_offers(queryset)
            return queryset
        except Customer.DoesNotExist:
            booleano = False
            Assertions.assert_true_raise400(booleano, {'error': 'ERROR_NO_CUSTOMER_FOUND'})
