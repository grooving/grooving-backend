from django.shortcuts import render
from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from .serializers import ArtistInfoSerializer
from django.core.exceptions import PermissionDenied
from Grooving.models import Artist, ArtisticGender
from rest_framework import viewsets
from utils.Assertions import assert_true
from .serializers import ListArtistSerializer
from rest_framework.response import Response


class GetPersonalInformationOfArtist(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ArtistInfoSerializer

    def get(self, name):

        if self.request.user.is_authenticated:
            loggeduser = self.request.user
            try:
                queryset = Artist.objects.get(user=loggeduser)
                serializer = ArtistInfoSerializer(queryset)
                return Response(serializer.data)
            except ObjectDoesNotExist:
                raise PermissionDenied()
        else:
            raise PermissionDenied()


class ListArtist(generics.ListAPIView):
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
                    artists = []
                    artists.extend(Artist.objects.filter(portfolio__artisticGender=artgen))
                    if len(ArtisticGender.objects.filter(parentGender=artgen)) != 0 and artgen is not None:
                        #Se busca los artistas cuyos estilos artisticos coinciden con el padre

                        children = []
                        children.extend(list(ArtisticGender.objects.filter(parentGender=artgen)))

                        #se hace el mismo proceso en bucle
                        for gender in children:
                            artists.extend(Artist.objects.filter(portfolio__artisticGender=gender))
                            numChildren = []
                            numChildren.extend(ArtisticGender.objects.filter(parentGender=gender))
                            #Si tiene hijos, se añaden
                            if len(numChildren) != 0:
                                children.extend(numChildren)
                        queryset = artists
                    else:
                        artgen = ArtisticGender.objects.get(name=artisticgender)
                        queryset = Artist.objects.filter(portfolio__artisticGender=artgen)
                #Si el padre no existe:
                except ObjectDoesNotExist:
                    queryset = []
                    return queryset
                if artisticname:
                    queryset = queryset.filter(portfolio__artisticName=artisticname)
        else:
            queryset = Artist.objects.all()
        return queryset
