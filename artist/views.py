from rest_framework import generics
from .serializers import ArtistInfoSerializer
from Grooving.models import Artist
from utils.authentication_utils import get_user_type, get_logged_user
from .serializers import ListArtistSerializer
from rest_framework.response import Response
from rest_framework import status
from utils.Assertions import Assertions
from artist.serializers import ArtistSerializer
from utils.searcher.searcher import search
from artist.internationalization import translate
from utils.utils import check_accept_language, check_special_characters_and_numbers


class GetPersonalInformationOfArtist(generics.ListAPIView):
    serializer_class = ArtistInfoSerializer

    def get(self, request, *args, **kwargs):
        language = check_accept_language(request)

        user = get_logged_user(self.request)
        user_type = get_user_type(user)

        Assertions.assert_true_raise403(user is not None, translate(language, "ERROR_NOT_LOGGED_IN"))
        Assertions.assert_true_raise403(user_type == 'Artist', translate(language, "ERROR_NOT_AN_ARTIST"))

        try:
            artist = Artist.objects.get(user_id=user.user_id)
            serializer = ArtistInfoSerializer(artist)
            return Response(serializer.data)
        except Artist.DoesNotExist:
            Assertions.assert_true_raise400(False, translate(language, "ERROR_NO_ARTIST_FOUND"))


class ListArtist(generics.ListAPIView):
    model = Artist
    serializer_class = ListArtistSerializer

    def get_queryset(self):
        artistic_name = self.request.query_params.get('artisticName')
        artistic_gender = self.request.query_params.get('artisticGender')
        zone = self.request.query_params.get('zone')
        order = self.request.query_params.get('order')

        queryset = search(artisticName=artistic_name, categoria=artistic_gender, zone=zone, order=order)
        return queryset


class ArtistRegister(generics.CreateAPIView):
    serializer_class = ArtistSerializer

    def get_object(self, request, pk=None):
        language = check_accept_language(request)
        try:
            return Artist.objects.get(pk=pk)
        except Artist.DoesNotExist:
            Assertions.assert_true_raise404(False, translate(language, "ERROR_NO_ARTIST_FOUND"))

    def post(self, request, *args, **kwargs):
        language = check_accept_language(request)

        Assertions.assert_true_raise400(len(request.data) != 0, translate(language, "ERROR_NO_DATA_GIVEN"))
        user_type = None

        try:
            user = get_logged_user(request)
            user_type = get_user_type(user)
        except:
            pass
        if not user_type:
            serializer = ArtistSerializer(data=request.data, partial=True)
            if serializer.validate_artist(request):
                serializer.save(request)

                return Response(status=status.HTTP_201_CREATED)

        else:
            Assertions.assert_true_raise403(len(request.data) != 0, translate(language, "ERROR_MUST_LOGGED_OUT"))

    def put(self, request, pk=None):
        language = check_accept_language(request)
        Assertions.assert_true_raise400(len(request.data) != 0, translate(language, "ERROR_EMPTY_FORM"))
        Assertions.assert_true_raise400(request.data.get("artisticName"),
                                        translate(language, "ERROR_EMPTY_ARTISTIC_NAME"))
        Assertions.assert_true_raise400(check_special_characters_and_numbers(request.data.get("first_name")),
                                        translate(language, "ERROR_FIRST_NAME_SPECIAL_CHARACTERS"))
        Assertions.assert_true_raise400(check_special_characters_and_numbers(request.data.get("last_name")),
                                        translate(language, "ERROR_LAST_NAME_SPECIAL_CHARACTERS"))

        if pk is None:
            pk = self.kwargs['pk']

        artist = self.get_object(request, pk)
        artist_or_customer = get_logged_user(request)

        Assertions.assert_true_raise403(artist_or_customer, translate(language, "ERROR_ARTIST_NOT_LOGGED"))
        Assertions.assert_true_raise403(artist_or_customer.user.id == artist.user.id,
                                        translate(language, "ERROR_IT_ISNT_YOUR_PERSONAL_INFO"))

        serializer = ArtistSerializer(artist, data=request.data, partial=True)
        serializer.is_valid(True)
        artist = serializer.update(request, pk)

        artist.save()

        return Response(status=status.HTTP_200_OK)
