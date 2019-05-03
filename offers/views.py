from Grooving.models import Offer, Artist, Customer
from rest_framework import generics
from .serializers import ListArtistOffersSerializer, ListCustomerOffersSerializer
from utils.authentication_utils import get_user_type, get_logged_user
from utils.utils import auto_update_old_offers, cancel_offers_with_no_user
from utils.Assertions import Assertions
from utils.utils import check_accept_language
from offers.internationalization import translate


class ListArtistOffers(generics.ListAPIView):

    serializer_class = ListArtistOffersSerializer

    def get_queryset(self):
        language = check_accept_language(self.request)
        user = get_logged_user(self.request)
        user_type = get_user_type(user)

        Assertions.assert_true_raise403(user is not None, translate(keyLanguage=language,
                                                      keyToTranslate= "ERROR_NOT_LOGGED_IN"))
        Assertions.assert_true_raise403(user_type == 'Artist', translate(keyLanguage=language,
                                                      keyToTranslate="ERROR_NOT_AN_ARTIST"))
        try:
            artist = Artist.objects.get(user_id=user.user_id)

            queryset = Offer.objects.filter(paymentPackage__portfolio__artist=artist).order_by('date')
            auto_update_old_offers(queryset)
            cancel_offers_with_no_user(queryset)
            return queryset
        except Artist.DoesNotExist:
            booleano = False
            Assertions.assert_true_raise400(booleano, translate(keyLanguage=language,
                                                      keyToTranslate = "ERROR_NO_ARTIST_FOUND"))


class ListCustomerOffers(generics.ListAPIView):

    serializer_class = ListCustomerOffersSerializer

    def get_queryset(self):
        language = check_accept_language(self.request)
        user = get_logged_user(self.request)
        user_type = get_user_type(user)
        Assertions.assert_true_raise403(user is not None, translate(keyLanguage=language,
                                                      keyToTranslate="ERROR_NOT_LOGGED_IN"))
        Assertions.assert_true_raise403(user_type == 'Customer', translate(keyLanguage=language,
                                                      keyToTranslate="ERROR_NOT_A_CUSTOMER"))
        try:
            customer = Customer.objects.get(user_id=user.user_id)
            queryset = Offer.objects.filter(eventLocation__customer=customer).order_by('date')
            auto_update_old_offers(queryset)
            cancel_offers_with_no_user(queryset)
            return queryset
        except Customer.DoesNotExist:
            booleano = False
            Assertions.assert_true_raise400(booleano, translate(keyLanguage=language,
                                                      keyToTranslate= "ERROR_NO_CUSTOMER_FOUND"))
