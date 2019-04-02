from rest_framework import serializers
from Grooving.models import Rating, Artist, Offer
from portfolio.serializers import UserSerializer
from utils.authentication_utils import get_logged_user, get_user_type
from utils.Assertions import assert_true
from django.http import Http404
from django.core.exceptions import PermissionDenied


class ListRatingSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Rating
        fields = ('score', 'comment')


class CustomerRatingSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Rating
        fields = ('score', 'comment')

    def validate(self, request, pk):
        # Primero, se mira si el que intenta realizar la acción es un customer.

        user = get_logged_user(request)
        user_type = get_user_type(user)

        #       Si no es Customer, se le bloquea el paso

        assert_true(user_type == 'Customer', "You are not a customer, and thus aren't allowed to be here.")

        #       Si lo es, se mira que sea, de hecho, el que creó la oferta en primer lugar
        #       Se obtiene la oferta que se quiere valorar y se toma su Customer

        try:
            #   Se busca la oferta. Si no existe, error 404
            offer = Offer.objects.get(id=pk)
            assert_true(user.user_id == offer.eventLocation.customer.user.id, "You are not the owner of this offer.")

            #       Ahora se mira si la oferta está en estado PAYMENT_MADE

            assert_true(offer.status == 'PAYMENT_MADE', 'This offer is not ready to receive a rating yet.')

            #       Finalmente, se mira si ha votado ya o no

            assert_true(offer.rating is None, 'This offer has already be rated. You cannot rate it twice.')

            #       Django tiene protección ante XSS activada por defecto por HTML escaping. Además, el comentario puede
            #       ser nulo.

            #       Salimos de la función

            return True
        except Offer.DoesNotExist:
            raise Http404


class ArtistRatingSerializer(serializers.HyperlinkedModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Artist
        fields = ('id', 'rating', 'user', 'portfolio')
