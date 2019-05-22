from Grooving.models import User, Actor
from utils.Assertions import Assertions
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from .serializers import LanguageChooserArtistSerializer, LanguageChooserCustomerSerializer, LanguageChooserAdminSerializer
from user.serializers import UserSerializer
from utils.authentication_utils import get_logged_user, get_user_type, get_admin_2
from languageChooser.internationalization import translate
from utils.utils import check_accept_language


class LanguageChooser(generics.ListAPIView):

    serializer_class = LanguageChooserArtistSerializer

    def get(self, request, *args, **kwargs):
        querysetAdmin = get_admin_2(request)
        queryset = get_logged_user(request)
        language = check_accept_language(request)
        Assertions.assert_true_raise403(queryset or querysetAdmin, translate(language, 'ERROR_NOT_LOGGED_IN'))
        user_type = get_user_type(queryset)
        if user_type == 'Artist':
            serializer = LanguageChooserArtistSerializer(data=request.data, partial=True)
        elif user_type == 'Customer':
            serializer = LanguageChooserCustomerSerializer(data=request.data, partial=True)
        else:
            serializer = LanguageChooserAdminSerializer(data=request.data, partial=True)

        if serializer.validate(request):

            language = request.query_params.get('lang').lower()

            if queryset:
                queryset.language = language
                queryset.save()
            elif querysetAdmin:
                querysetAdmin.language = language
                querysetAdmin.save()

            if user_type == 'Artist':
                serialized = LanguageChooserArtistSerializer(queryset)
            elif user_type == 'Customer':
                serialized = LanguageChooserCustomerSerializer(queryset)
            else:
                serialized = LanguageChooserAdminSerializer(querysetAdmin)

            return Response(serialized.data, status=status.HTTP_200_OK)
        else:
            return Response(translate(language,'ERROR_VALIDATE'), status=status.HTTP_400_BAD_REQUEST)
