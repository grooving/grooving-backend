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
        Assertions.assert_true_raise401(rating.score, {'error': 'You must give a score to this artist.'})

        Assertions.assert_true_raise401(isinstance(rating.score, int), {'error': 'The score must be a number with no decimals.'})
        Assertions.assert_true_raise401(rating.score >= 1 and rating.score <= 5, {'error': 'The rating cannot be less than 1 or more than 5 points.'})

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
        Assertions.assert_true_raise403(user is not None, {'error': 'You must be logged in to access this page.'})
        Assertions.assert_true_raise403(user_type == 'Customer', {'error': 'You are not a customer, and thus are not allowed to be here.'})

        #       Si lo es, se mira que sea, de hecho, el que creó la oferta en primer lugar
        #       Se obtiene la oferta que se quiere valorar y se toma su Customer

        #   Se busca la oferta. Si no existe, error 400
        try:

            offer = Offer.objects.get(id=pk)
            Assertions.assert_true_raise403(user.user_id == offer.eventLocation.customer.user.id,
                                            {'error': 'You are not the owner of this offer.'})

            #       Ahora se mira si la oferta está en estado PAYMENT_MADE

            Assertions.assert_true_raise401(offer.status == 'PAYMENT_MADE',
                                            {'error': 'This offer is not ready to receive a rating, since it has not been paid yet.'})

            #       Finalmente, se mira si ha votado ya o no

            Assertions.assert_true_raise401(offer.rating is None,
                                            {'error': 'This offer has already been rated. You cannot rate it twice.'})

            #       Django tiene protección ante XSS activada por defecto por HTML escaping. Además, el comentario puede
            #       ser nulo, si bien debe pasarse por la llamada aunque esté vacío.

            #       Salimos de la función

            return True

        except Offer.DoesNotExist:
            booleano = False
            Assertions.assert_true_raise400(booleano, {'error': 'This offer does not exist.'})






class ArtistRatingSerializer(serializers.HyperlinkedModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Artist
        fields = ('id', 'rating', 'user', 'portfolio')
