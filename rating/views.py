from Grooving.models import Rating, Offer
from rest_framework.response import Response
from rest_framework import generics, status
from rating.serializers import CustomerRatingSerializer, ListRatingSerializer


class GetRatings(generics.ListAPIView):

    model = Rating
    serializer_class = ListRatingSerializer
    authentication_classes = []

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
        serializer.validate(request, pk) #  "Some of the conditions to do this action aren't fulfilled.")

        rating = serializer.save()
        ratingChecked = CustomerRatingSerializer(rating)
        offer = Offer.objects.get(id=pk)
        offer.rating = rating
        offer.save()
        artist = offer.paymentPackage.portfolio.artist

        offersWithArtist = Offer.objects.filter(paymentPackage__portfolio__artist=artist)
        numRaters = 0

        for offer in offersWithArtist:

            if offer.rating is not None:
                numRaters = numRaters + 1
        #   totalRating = offersWithArtist.annotate(Sum('rating'))

        #           Se comprueba que no sean 0 votos. No podemos dividir entre 0, o el universo explotará y los gatitos kawaiis
        #           de internet morirán

        if (numRaters == 0):

            artist.rating = rating.score
            artist.save()

        else:

            artist.rating = int(round((artist.rating * (numRaters - 1) + rating.score) / numRaters))

            artist.save()
        return Response(ratingChecked.data, status=status.HTTP_201_CREATED)
