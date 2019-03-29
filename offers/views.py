from Grooving.models import Offer, Artist, Customer
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from rest_framework import generics
from .serializers import ListOfferSerializer
from utils.authentication_utils import get_user_type, get_logged_user


class ListOffers(generics.ListAPIView):

    serializer_class = ListOfferSerializer

    def get_queryset(self):

        user = get_logged_user(self.request)
        user_type = get_user_type(user)

        if user_type == 'Artist':
            try:
                artist = Artist.objects.get(user_id=user.user_id)
                queryset = Offer.objects.filter(paymentPackage__portfolio__artist=artist)
                return queryset
            except ObjectDoesNotExist:
                try:
                    customer = Customer.objects.get(user_id=user.user_id)
                    queryset = Offer.objects.filter(eventLocation__customer=customer)
                    return queryset
                except ObjectDoesNotExist:
                    raise PermissionDenied("No tienes autorización para entrar aquí")
        else:
            if user_type == 'Customer':
                customer = Customer.objects.get(user_id=user.user_id)
                queryset = Offer.objects.filter(eventLocation__customer=customer)
#                serializer = ListOfferSerializer(queryset, many=True)
                return queryset
            else:
                # There are no offers matching the users; therefore, they have no offers linked to them. An empty list is given
                raise PermissionDenied("No tienes autorización para entrar aquí")
