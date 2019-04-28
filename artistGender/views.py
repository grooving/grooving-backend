from Grooving.models import ArtisticGender,Portfolio

from django.core.exceptions import PermissionDenied

from utils.authentication_utils import get_logged_user,get_user_type, get_admin_2
from utils.authentication_utils import get_logged_user, get_user_type, get_admin
from rest_framework.response import Response
from rest_framework import generics
from .serializers import ArtisticGenderSerializer, SearchGenreSerializer
from rest_framework import status
from utils.Assertions import Assertions
from utils.utils import check_accept_language
from .internationalization import translate


class ArtisticGenderManager(generics.RetrieveUpdateDestroyAPIView):

    queryset = ArtisticGender.objects.all()
    serializer_class = ArtisticGenderSerializer

    def get_object(self, pk=None):
        language = check_accept_language(self.request)
        if pk is None:
            pk = self.kwargs['pk']
        try:
            return ArtisticGender.objects.get(pk=pk)
        except ArtisticGender.DoesNotExist:
            raise Assertions.assert_true_raise404(False, translate(language, 'ERROR_ARTISTIC_GENRE_NOT_FOUND'))

    def get(self, request, pk=None, format=None):
        if pk is None:
            pk = self.kwargs['pk']
        language = check_accept_language(request)
        portfolio = self.get_object(pk)
        serializer = ArtisticGenderSerializer(portfolio,context={'language': language})
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        if pk is None:
            pk = self.kwargs['pk']
        language = check_accept_language(request)
        try:
            artisticGender = self.get_object(pk)
            loggedUser = get_admin_2(request)
            Assertions.assert_true_raise403(loggedUser, translate(language, "ERROR_NOT_AN_ADMIN"))
            id_request = request.data.get('id')
            pk_compare = int(pk)
            Assertions.assert_true_raise401(str(id_request).isdigit(), translate(language, "ERROR_INCORRECT_ID"))
            Assertions.assert_true_raise401(id_request == pk_compare, translate(language, "ERROR_INCORRECT_ID"))

            serializer = ArtisticGenderSerializer(artisticGender, data=request.data, partial=True,context={'language': language})
            if serializer.validate(request.data):
                serializer.is_valid()
                serializer.save(pk, loggedUser)
                return Response(status=status.HTTP_201_CREATED)
            else:
                raise Assertions.assert_true_raise400(False,
                                                      translate(language, 'ERROR_BAD_REQUEST'))
        except ArtisticGender.DoesNotExist:
            raise Assertions.assert_true_raise404(False, translate(language, 'ERROR_ARTISTIC_GENRE_NOT_FOUND'))


    def delete(self, request, pk=None, format=None):
        if pk is None:
            pk = self.kwargs['pk']
        language = check_accept_language(request)
        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, translate(language, "ERROR_NOT_AN_ADMIN"))

        artisticGender = self.get_object(pk)

        Assertions.assert_true_raise404(artisticGender, translate(language, "ERROR_GENRE_DOESNT_EXIST"))

        children = ArtisticGender.objects.filter(parentGender=artisticGender)

        for genre in children:
            self.cascadedelete(genre)

        artisticGender.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def cascadedelete(self, genre: ArtisticGender):
        language = check_accept_language(self.request)
        Assertions.assert_true_raise404(genre, translate(language, "ERROR_GENRE_DOESNT_EXIST"))
        children = ArtisticGender.objects.filter(parentGender=genre)

        for genre in children:
            self.cascadedelete(genre)
        genre.delete()


class CreateArtisticGender(generics.CreateAPIView):
    queryset = ArtisticGender.objects.all()
    serializer_class = ArtisticGenderSerializer

    def post(self, request, *args, **kwargs):

        admin = get_admin(request)
        language = check_accept_language(request)
        Assertions.assert_true_raise403(admin, translate(language, "ERROR_NOT_AN_ADMIN"))

        serializer = ArtisticGenderSerializer(data=request.data, partial=True,context={'language': language})
        if serializer.validate(request.data):
            serializer.is_valid()
            artisticGender = serializer.save()
            serialized = ArtisticGenderSerializer(artisticGender,context={'language': language})
            return Response(serialized.data, status=status.HTTP_201_CREATED)


class ListArtisticGenders(generics.RetrieveAPIView):

    serializer_class = SearchGenreSerializer

    def get_queryset(self):

        return ArtisticGender.objects.all()

    def get(self, request, *args, **kwargs):

        tree = request.query_params.get("tree", None)
        portfolio = request.query_params.get("portfolio", None)
        parentId = request.query_params.get("parentId", None)

        language = check_accept_language(request)

        genres = None
        if tree is None and portfolio is None and parentId is None:
            genres = list(ArtisticGender.objects.all())
            serializer = SearchGenreSerializer(genres, many=True,context={'language': language})
            genres = serializer.data
        elif tree == "true":
            Assertions.assert_true_raise400(portfolio is None and parentId is None, translate(language,"ERROR_ONLY_ONE_OPTION"))
            genres = SearchGenreSerializer.get_tree(language)
        elif parentId == "true":
            Assertions.assert_true_raise400(portfolio is None and tree is None, translate(language,"ERROR_ONLY_ONE_OPTION"))
            genres = SearchGenreSerializer.get_children(language)

        elif parentId is not None:
            try:
                parentId = int(parentId)
            except ValueError:
                Assertions.assert_true_raise400(False, translate(request.META['HTTP_ACCEPT_LANGUAGE'], "ERROR_INCORRECT_ID"))

            Assertions.assert_true_raise400(tree is None and portfolio is None, translate(language, "ERROR_ONLY_ONE_OPTION"))
            genres = SearchGenreSerializer.get_children(language,parentId)

        elif portfolio is not None:

            try:
                portfolio = int(portfolio)
            except ValueError:
                Assertions.assert_true_raise400(False, translate(language, "ERROR_INCORRECT_ID"))

            portfolio = Portfolio.objects.filter(pk=portfolio).first()
            Assertions.assert_true_raise404(portfolio,
                                            translate(language,'ERROR_NO_PORTFOLIO'))
            genres = portfolio.artisticGender.all()
            count = genres.count()
            child_genres = []
            for zone in genres:
                childs = SearchGenreSerializer.get_base_childs(zone, [])[0]
                if len(child_genres) == 0:
                    child_genres = childs
                else:
                    child_genres.extend(childs)

            serializer = SearchGenreSerializer(child_genres, many=True,context={'language': language})
            genres = serializer.data

        return Response(genres, status=status.HTTP_200_OK)