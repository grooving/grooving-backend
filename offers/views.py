from Grooving.models import Offer, Artist, Customer
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from rest_framework import generics
from .serializers import ListArtistOffersSerializer, ListCustomerOffersSerializer
from utils.authentication_utils import get_user_type, get_logged_user
from utils.utils import auto_update_old_offers

class ListArtistOffers(generics.ListAPIView):

    serializer_class = ListArtistOffersSerializer

    def get_queryset(self):

        user = get_logged_user(self.request)
        user_type = get_user_type(user)

        if user_type == 'Artist':
            artist = Artist.objects.get(user_id=user.user_id)
            queryset = Offer.objects.filter(paymentPackage__portfolio__artist=artist)
            auto_update_old_offers(queryset)
            return queryset
        else:
            raise PermissionDenied("No tienes autorización para entrar aquí")


class ListCustomerOffers(generics.ListAPIView):

    serializer_class = ListCustomerOffersSerializer

    def get_queryset(self):

        user = get_logged_user(self.request)
        user_type = get_user_type(user)

        if user_type == 'Customer':
            customer = Customer.objects.get(user_id=user.user_id)
            queryset = Offer.objects.filter(eventLocation__customer=customer)
            auto_update_old_offers(queryset)
            return queryset
        else:
            # There are no offers matching the users; therefore, they have no offers linked to them. An empty list is given
            raise PermissionDenied("No tienes autorización para entrar aquí")