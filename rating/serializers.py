from rest_framework import serializers
from Grooving.models import Rating, Artist, Offer
from portfolio.serializers import UserSerializer
from utils.authentication_utils import get_logged_user, get_user_type
from utils.Assertions import assert_true
from django.core.exceptions import ValidationError
from utils.Assertions import Assertions
from utils.utils import check_accept_language
from .internationalization import translate


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
        language = check_accept_language(request)
        #       Si no es Customer, se le bloquea el paso
        Assertions.assert_true_raise403(user is not None, translate(language, "ERROR_NOT_LOGGED_IN"))
        Assertions.assert_true_raise403(user_type == 'Customer', translate(language, "ERROR_NOT_A_CUSTOMER"))

        #       Si lo es, se mira que sea, de hecho, el que creó la oferta en primer lugar
        #       Se obtiene la oferta que se quiere valorar y se toma su Customer



        #   Se busca la oferta. Si no existe, error 400
        try:

            offer = Offer.objects.get(id=pk)
            Assertions.assert_true_raise403(user.user_id == offer.eventLocation.customer.user.id,
                                            translate(language, "ERROR_OFFER_NOT_OWNED"))

            #       Ahora se mira si la oferta está en estado PAYMENT_MADE

            Assertions.assert_true_raise401(offer.status == 'PAYMENT_MADE',
                                            translate(language, "ERROR_OFFER_NOT_READY"))

            #       Finalmente, se mira si ha votado ya o no

            Assertions.assert_true_raise401(offer.rating is None,
                                            translate(language, "ERROR_OFFER_ALREADY_RATED"))

            #       Django tiene protección ante XSS activada por defecto por HTML escaping. Además, el comentario puede
            #       ser nulo, si bien debe pasarse por la llamada aunque esté vacío.

            #Se comprueba que la oferta no este unida a un artista que se haya dado de baja. Para ello, miramos si el portfolio esta hidden

            portfolio = offer.paymentPackage.portfolio

            Assertions.assert_true_raise400(portfolio.isHidden is False, translate(language, "ERROR_NO_USER"))

            Assertions.assert_true_raise401(request.data.get('score'), translate(language, "ERROR_NO_SCORE"))

            Assertions.assert_true_raise401(isinstance(request.data['score'], int),translate(language, "ERROR_DECIMAL_SCORE"))
            Assertions.assert_true_raise401(request.data['score'] >= 1 and request.data['score'] <= 5,
                                            translate(language, "ERROR_RATING_OUT_OF_RANGE"))

            #       Salimos de la función

            return True

        except Offer.DoesNotExist:

            Assertions.assert_true_raise400(False, translate(language, "ERROR_OFFER_NOT_FOUND"))


class ArtistRatingSerializer(serializers.HyperlinkedModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Artist
        fields = ('id', 'rating', 'user', 'portfolio')
