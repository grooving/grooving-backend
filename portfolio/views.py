from Grooving.models import Portfolio, Artist
from utils.authentication_utils import get_logged_user, get_user_type
from rest_framework.response import Response
from rest_framework import generics
from .serializers import PortfolioSerializer
from rest_framework import status
from utils.Assertions import Assertions
from utils.utils import check_accept_language
from .internationalization import translate


class PortfolioManager(generics.RetrieveUpdateDestroyAPIView):

    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer

    def get_object(self, pk=None, language='en'):
        if pk is None:
            pk = self.kwargs['pk']
        try:
            return Portfolio.objects.get(pk=pk)
        except Portfolio.DoesNotExist:
            Assertions.assert_true_raise404(False,
                                            translate(language, 'ERROR_PORTFOLIO_NOT_FOUND'))

    def get(self, request, pk=None, format=None):
        if pk is None:
            pk = self.kwargs['pk']
        portfolio = self.get_object(pk)
        serializer = PortfolioSerializer(portfolio, partial=True)
        return Response(serializer.data)

    def put(self, request, pk=None):

        language = check_accept_language(request)

        if pk is None:
            pk = self.kwargs['pk']
        if Portfolio.objects.filter(pk=pk).first():
            portfolio = Portfolio.objects.filter(pk=pk).first()
            loggedUser = get_logged_user(request)
            user_type = get_user_type(loggedUser)
            artist = Artist.objects.filter(portfolio=portfolio).first()
            if loggedUser is not None and loggedUser.id == artist.id and user_type == "Artist":
                serializer = PortfolioSerializer(portfolio, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save(loggedUser, language=language)
                    portfolio = self.get_object(pk, language=language)
                    serializer = PortfolioSerializer(portfolio, data=serializer.data, partial=True)
                    serializer.is_valid()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                raise Assertions.assert_true_raise403(False, translate(language, 'ERROR_NOT_LOGGED_OR_NOT_OWNER'))
        else:
            return Assertions.assert_true_raise404(False, translate(language, 'ERROR_PORTFOLIO_NOT_FOUND'))

    def delete(self, request, pk=None, format=None):

        language = check_accept_language(request)

        if pk is None:
            pk = self.kwargs['pk']
        portfolio = self.get_object(pk, language=language)
        portfolio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



