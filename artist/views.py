from django.shortcuts import render
from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from .serializers import ArtistInfoSerializer
from django.core.exceptions import PermissionDenied
from Grooving.models import Artist, ArtisticGender
from rest_framework import viewsets
from utils.authentication_utils import get_user_type, get_logged_user, is_user_authenticated
from .serializers import ListArtistSerializer
from rest_framework.response import Response


class GetPersonalInformationOfArtist(generics.ListAPIView):

    serializer_class = ArtistInfoSerializer

    def get(self, request, *args, **kwargs):

        user = get_logged_user(self.request)
        user_type = get_user_type(user)
        if user_type == 'Artist':
            artist = Artist.objects.get(user_id=user.user_id)
            serializer = ArtistInfoSerializer(artist)
            return Response(serializer.data)
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
                queryset = Artist.objects.filter(portfolio__artisticName__icontains=artisticname)
            if artisticgender:
                try:
                    artgen = ArtisticGender.objects.filter(name__icontains=artisticgender)
                    artists = []
                    artistasEncontrados = Artist.objects.filter(portfolio__artisticGender=artgen)
                    artists.append(artistasEncontrados)
                    if len(ArtisticGender.objects.filter(parentGender__in=artgen)) != 0 and artgen is not None:
                        #Se busca los artistas cuyos estilos artisticos coinciden con el padre

                        children = []
                        children.extend(list(ArtisticGender.objects.filter(parentGender__in=artgen)))

                        #se hace el mismo proceso en bucle
                        for gender in children:
                            artists.extend(Artist.objects.filter(portfolio__artisticGender=gender).distinct('portfolio'))
                            numChildren = []
                            numChildren.extend(ArtisticGender.objects.filter(parentGender__name__icontains=gender.name))
                            #Si tiene hijos, se añaden
                            if len(numChildren) != 0:
                                children.extend(numChildren)
                        queryset = artists
                    else:
                        artgen = ArtisticGender.objects.filter(name__icontains=artisticgender)
                        queryset = Artist.objects.filter(portfolio__artisticGender__in=artgen).distinct(
                            'portfolio')
                #Si el padre no existe:
                except ObjectDoesNotExist:
                    queryset = []
                    return queryset
                if artisticname:
                    queryset = queryset.filter(portfolio__artisticName__icontains=artisticname)
        else:
            queryset = Artist.objects.all()
        return queryset
