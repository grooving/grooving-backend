from rest_framework import serializers
from Grooving.models import Rating, Artist, Offer
from portfolio.serializers import UserSerializer
from utils.authentication_utils import get_logged_user, get_user_type
from utils.Assertions import assert_true
from django.core.exceptions import ValidationError
from utils.Assertions import Assertions


class ListRatingSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Rating
        fields = ('id', 'score', 'comment')


class CustomerRatingSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Rating
        fields = ('id', 'score', 'comment')

    @staticmethod
    def _service_create(json: dict, rating: Rating):

        rating.score = json.get('score')
        Assertions.assert_true_raise401(rating.score, {'error': 'ERROR_NO_SCORE'})

        Assertions.assert_true_raise401(isinstance(rating.score, int), {'error': 'ERROR_DECIMAL_SCORE'})
        Assertions.assert_true_raise401(rating.score >= 1 and rating.score <= 5, {'error': 'ERROR_RATING_OUT_OF_RANGE'})

        rating.comment = json.get('comment')

        rating.save()
        return rating

    def save(self, pk=None, logged_user=None):
        if self.initial_data.get('id') is None and pk is None:
            # creation
            rating = Rating()
            rating = self._service_create(self.initial_data, rating)
        return rating

    def validate(self, request, pk): #  Aquí habia un pk
        # Primero, se mira si el que intenta realizar la acción es un customer.

        user = get_logged_user(request)
        user_type = get_user_type(user)

        #       Si no es Customer, se le bloquea el paso
        Assertions.assert_true_raise403(user is not None, {'error': 'ERROR_NOT_LOGGED_IN'})
        Assertions.assert_true_raise403(user_type == 'Customer', {'error': 'ERROR_NOT_A_CUSTOMER'})

        #       Si lo es, se mira que sea, de hecho, el que creó la oferta en primer lugar
        #       Se obtiene la oferta que se quiere valorar y se toma su Customer

        #   Se busca la oferta. Si no existe, error 400
        try:

            offer = Offer.objects.get(id=pk)
            Assertions.assert_true_raise403(user.user_id == offer.eventLocation.customer.user.id,
                                            {'error': 'ERROR_OFFER_NOT_OWNED'})

            #       Ahora se mira si la oferta está en estado PAYMENT_MADE

            Assertions.assert_true_raise401(offer.status == 'PAYMENT_MADE',
                                            {'error': 'ERROR_OFFER_NOT_READY'})

            #       Finalmente, se mira si ha votado ya o no

            Assertions.assert_true_raise401(offer.rating is None,
                                            {'error': 'ERROR_OFFER_ALREADY_RATED'})

            #       Django tiene protección ante XSS activada por defecto por HTML escaping. Además, el comentario puede
            #       ser nulo, si bien debe pasarse por la llamada aunque esté vacío.

            #Se comprueba que la oferta no este unida a un artista que se haya dado de baja. Para ello, miramos si el portfolio esta hidden

            portfolio = offer.paymentPackage.portfolio

            Assertions.assert_true_raise400(portfolio.isHidden is False, {'error': 'ERROR_NO_USER'})

            #       Salimos de la función

            return True

        except Offer.DoesNotExist:
            booleano = False
            Assertions.assert_true_raise400(booleano, {'error': 'ERROR_OFFER_NOT_FOUND'})






class ArtistRatingSerializer(serializers.HyperlinkedModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Artist
        fields = ('id', 'rating', 'user', 'portfolio')
