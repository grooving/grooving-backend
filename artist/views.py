from rest_framework import generics
from .serializers import ArtistInfoSerializer
from django.core.exceptions import PermissionDenied
from Grooving.models import Artist
from utils.authentication_utils import get_user_type, get_logged_user
from .serializers import ListArtistSerializer
from rest_framework.response import Response
from rest_framework import status
from utils.Assertions import Assertions
from artist.serializers import ArtistSerializer
from django.http import Http404
from utils.searcher.searcher import search


class GetPersonalInformationOfArtist(generics.ListAPIView):

    serializer_class = ArtistInfoSerializer

    def get(self, request, *args, **kwargs):

        user = get_logged_user(self.request)
        user_type = get_user_type(user)
        Assertions.assert_true_raise403(user is not None, {'error': 'You must be logged in to access this page.'})
        Assertions.assert_true_raise403(user_type == 'Artist', {'error': 'You are not an artist.'})
        try:
            artist = Artist.objects.get(user_id=user.user_id)
            serializer = ArtistInfoSerializer(artist)
            return Response(serializer.data)
        except Artist.DoesNotExist:
            booleano = False
            Assertions.assert_true_raise400(booleano, {'error': 'The requested artist does not exist.'})


class ListArtist(generics.ListAPIView):
    model = Artist
    serializer_class = ListArtistSerializer

    def get_queryset(self):

        artisticname = self.request.query_params.get('artisticName')
        artisticgender = self.request.query_params.get('artisticGender')
        zone = self.request.query_params.get('zone')
        order = self.request.query_params.get('order')
        """
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
                        # Se busca los artistas cuyos estilos artisticos coinciden con el padre

                        children = []
                        children.extend(list(ArtisticGender.objects.filter(parentGender__in=artgen)))

                        # se hace el mismo proceso en bucle
                        for gender in children:
                            artists.extend(Artist.objects.filter(portfolio__artisticGender=gender).distinct('portfolio'))
                            numChildren = []
                            numChildren.extend(ArtisticGender.objects.filter(parentGender__name__icontains=gender.name))
                            # Si tiene hijos, se añaden
                            if len(numChildren) != 0:
                                children.extend(numChildren)
                        queryset = artists
                    else:
                        artgen = ArtisticGender.objects.filter(name__icontains=artisticgender)
                        queryset = Artist.objects.filter(portfolio__artisticGender__in=artgen).distinct(
                            'portfolio')
                # Si el padre no existe:
                except ObjectDoesNotExist:
                    queryset = []
                    return queryset
                if artisticname:
                    queryset = queryset.filter(portfolio__artisticName__icontains=artisticname)
        else:
            queryset = Artist.objects.all()
        """
        queryset = search(artisticName=artisticname, categoria=artisticgender, zone=zone, order=order)
        return queryset


class ArtistRegister(generics.CreateAPIView):

    serializer_class = ArtistSerializer

    def get_object(self, pk=None):
        try:
            return Artist.objects.get(pk=pk)
        except Artist.DoesNotExist:
            raise Http404

    def post(self, request, *args, **kwargs):
        Assertions.assert_true_raise400(len(request.data) != 0, {'error': "Empty form is not valid"})
        user_type = None
        try:
            user = get_logged_user(request)
            user_type = get_user_type(user)
        except:
            pass
        if not user_type:
            serializer = ArtistSerializer(data=request.data, partial=True)
            if serializer.validate_artist(request):
                serializer.save()

                return Response(status=status.HTTP_201_CREATED)

        else:
            raise PermissionDenied("You must be unlogged to do this action")

    def put(self, request, pk=None):
        if pk is None:
            pk = self.kwargs['pk']
        Assertions.assert_true_raise400(len(request.data) != 0, {'error': "Empty form is not valid"})
        artist = Artist.objects.get(pk=pk)
        articustomer = get_logged_user(request)

        Assertions.assert_true_raise403(articustomer.user.id == artist.user.id,
                                        {'code': 'You can only change your personal info'})
        serializer = ArtistSerializer(artist, data=request.data, partial=True)
        Assertions.assert_true_raise400(serializer.is_valid(), {"code": "invalid data"})
        artist = serializer.update(pk)

        artist.save()
        return Response(status=status.HTTP_200_OK)

