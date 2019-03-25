from Grooving.models import Artist, ArtisticGender
from rest_framework import viewsets
from .serializers import ListArtistSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response


class ListArtist(viewsets.ModelViewSet):
    model = Artist
    serializer_class = ListArtistSerializer

    def get_queryset(self):

        artisticname = self.request.query_params.get('artisticName')
        artisticgender = self.request.query_params.get('artisticGender')
        if artisticname or artisticgender:
            if artisticname:
                queryset = Artist.objects.filter(portfolio__artisticName=artisticname)
            if artisticgender:
                try:
                    artgen = ArtisticGender.objects.get(name=artisticgender)
                except ObjectDoesNotExist:
                    queryset = []
                    return queryset
                if artisticname:
                    queryset = queryset.filter(portfolio__artisticGender=artgen)
                else:
                    queryset = Artist.objects.filter(portfolio__artisticGender=artgen)
        else:
            queryset = Artist.objects.all()
        return queryset
