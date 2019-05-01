from Grooving.models import PortfolioModule, Artist
from rest_framework.response import Response
from rest_framework import generics
from .serializers import PortfolioModuleSerializer
from rest_framework import status
from django.core.exceptions import PermissionDenied
from utils.authentication_utils import get_logged_user,get_user_type,is_user_authenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from utils.Assertions import Assertions
from utils.utils import check_accept_language
from .internationalization import translate


class PortfolioModuleManager(generics.RetrieveUpdateDestroyAPIView):

    queryset = PortfolioModule.objects.all()
    serializer_class = PortfolioModuleSerializer

    def get_object(self, pk=None):
        language = check_accept_language(self.request)
        if pk is None:
            pk = self.kwargs['pk']
        try:
            return PortfolioModule.objects.get(pk=pk)
        except PortfolioModule.DoesNotExist:
            raise Assertions.assert_true_raise404(False, translate(language, 'ERROR_PORTFOLIOMODULE_NOT_FOUND'))

    def get(self, request, pk=None, format=None):
        if pk is None:
            pk = self.kwargs['pk']
        portfolioModule = self.get_object(pk)
        serializer = PortfolioModuleSerializer(portfolioModule)
        return Response(serializer.data)

    def put(self, request, pk=None):
        language = check_accept_language(request)
        if pk is None:
            pk = self.kwargs['pk']
        portfolioModule = self.get_object(pk=pk)
        loggedUser = get_logged_user(request)
        artist = Artist.objects.filter(portfolio=portfolioModule.portfolio).first()
        if loggedUser is not None and loggedUser.id == artist.id:
            serializer = PortfolioModuleSerializer(portfolioModule, data=request.data, partial=True)
            if serializer.validate(request):
                module = serializer.save(pk, logged_user=request.user)
                serialized = PortfolioModuleSerializer(module)
                return Response(serialized.data, status=status.HTTP_200_OK)
            else:
                raise Assertions.assert_true_raise400(False, translate(language, "ERROR_INVALID_PARAMETERS"))
        else:
            raise Assertions.assert_true_raise403(False, translate(language, "ERROR_NOT_AN_ARTIST"))

    def delete(self, request, pk=None, format=None):

        if pk is None:
            pk = self.kwargs['pk']
        portfolioModule = self.get_object(pk=pk)
        portfolioModule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreatePortfolioModule(generics.CreateAPIView):
    queryset = PortfolioModule.objects.all()
    serializer_class = PortfolioModuleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):

        language = check_accept_language(request)
        user = get_logged_user(request)
        user_type = get_user_type(user)
        Assertions.assert_true_raise403(user and user_type == 'Artist', translate(language, "ERROR_NOT_AN_ARTIST"))
        serializer = PortfolioModuleSerializer(data=request.data, partial=True)

        if serializer.validate(request):
            module = serializer.save(logged_user=request.user)
            serialized = PortfolioModuleSerializer(module)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
