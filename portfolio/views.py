from Grooving.models import Portfolio, Artist
from utils.authentication_utils import get_logged_user, get_user_type
from rest_framework.response import Response
from rest_framework import generics
from .serializers import PortfolioSerializer
from rest_framework import status
from utils.Assertions import Assertions
from .internationalization import translate
from utils.utils import check_accept_language


class PortfolioManager(generics.RetrieveUpdateDestroyAPIView):

    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer

    def get_object(self, pk=None):
        if pk is None:
            pk = self.kwargs['pk']
        language = check_accept_language(self.request)
        try:
            return Portfolio.objects.get(pk=pk)
        except Portfolio.DoesNotExist:
            Assertions.assert_true_raise404(False,
                                            translate(language, 'ERROR_NO_PORTFOLIO'))

    def get(self, request, pk=None, format=None):
        if pk is None:
            pk = self.kwargs['pk']
        portfolio = self.get_object(pk)
        serializer = PortfolioSerializer(portfolio, partial=True)
        return Response(serializer.data)

    def put(self, request, pk=None):
        if pk is None:
            pk = self.kwargs['pk']
        language = check_accept_language(self.request)
        if Portfolio.objects.filter(pk=pk).first():
            portfolio = Portfolio.objects.filter(pk=pk).first()
            loggedUser = get_logged_user(request)
            user_type = get_user_type(loggedUser)
            artist = Artist.objects.filter(portfolio=portfolio).first()
            Assertions.assert_true_raise403(loggedUser is not None, translate(language, 'ERROR_NOT_LOGGED_IN'))
            if loggedUser.id == artist.id and user_type == "Artist":
                serializer = PortfolioSerializer(portfolio, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save(loggedUser,language)
                    portfolio = self.get_object(pk)
                    serializer = PortfolioSerializer(portfolio, data=serializer.data, partial=True)
                    serializer.is_valid()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                raise Assertions.assert_true_raise403(False, translate(language, 'ERROR_NO_PORTFOLIO_USER'))
        else:
            return Assertions.assert_true_raise404(False, translate(language, 'ERROR_NO_PORTFOLIO'))

    def delete(self, request, pk=None, format=None):
        if pk is None:
            pk = self.kwargs['pk']
        portfolio = self.get_object(pk)
        portfolio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



