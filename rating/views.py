from Grooving.models import Rating, Artist, Offer
from utils.authentication_utils import get_logged_user,get_user_type
from rest_framework.response import Response
from rest_framework import generics
from django.http import Http404
from rating.serializers import CustomerRatingSerializer, ListRatingSerializer
from utils.Assertions import assert_true
from rest_framework import status


class GetRatings(generics.ListAPIView):

    model = Rating
    serializer_class = ListRatingSerializer

    """
    def get_object(self, pk=None):

        if pk is None:
            pk = self.kwargs['pk']
        try:
            rating = Rating.objects.filter(id=pk)
            return rating
        except Rating.DoesNotExist:
            raise Http404
    """
    def get_queryset(self, pk=None):

        #   el PK es de un artist cuyos ratings queremos obtener

        if pk is None:
            pk = self.kwargs['pk']

        offers = Offer.objects.filter(paymentPackage__portfolio__artist__user__id=pk)

        rating = []

        #   De cada oferta se extrae su rating, que es de este artista
        for offer in offers:

            if offer.rating is not None:

                rating.append(offer.rating)

        return rating


class PostRating(generics.CreateAPIView):

    serializer_class = CustomerRatingSerializer

    #Esto sólo lo puede hacer un customer, y se tomará la pk de la oferta en cuestión

    def post(self, request, *args, **kwargs):

        pk = self.kwargs['pk']

        serializer = CustomerRatingSerializer(data=request.data)
        assert_true(serializer.validate(request, pk), "Some of the conditions to do this action aren't fulfilled.")
        rating = serializer.save()
        ratingChecked = CustomerRatingSerializer(rating)

        return Response(ratingChecked.data, status=status.HTTP_201_CREATED)
