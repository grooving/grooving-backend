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

        Assertions.assert_true_raise403(user is not None, {'error': 'You must be logged in to access this page.'})
        Assertions.assert_true_raise403(user_type == 'Artist', {'error': 'You are not an artist.'})
        try:
            artist = Artist.objects.get(user_id=user.user_id)

            queryset = Offer.objects.filter(paymentPackage__portfolio__artist=artist)
            auto_update_old_offers(queryset)
            return queryset
        except Artist.DoesNotExist:
            booleano = False
            Assertions.assert_true_raise400(booleano, {'error': 'This artist does not exist.'})


class ListCustomerOffers(generics.ListAPIView):

    serializer_class = ListCustomerOffersSerializer

    def get_queryset(self):

        user = get_logged_user(self.request)
        user_type = get_user_type(user)
        Assertions.assert_true_raise403(user is not None, {'error': 'You must be logged in to access this page.'})
        Assertions.assert_true_raise403(user_type == 'Customer', {'error': 'You are not a customer.'})
        try:
            customer = Customer.objects.get(user_id=user.user_id)
            queryset = Offer.objects.filter(eventLocation__customer=customer)
            auto_update_old_offers(queryset)
            return queryset
        except Customer.DoesNotExist:
            booleano = False
            Assertions.assert_true_raise400(booleano, {'error': 'This customer does not exist.'})
