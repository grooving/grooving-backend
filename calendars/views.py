from Grooving.models import Calendar,Portfolio,Artist
from rest_framework.response import Response
from rest_framework import generics
from .serializers import CalendarSerializer
from rest_framework import status
from utils.authentication_utils import get_logged_user,get_user_type
from utils.Assertions import Assertions
from utils.utils import check_accept_language
from .internationalization import translate
from django.core.exceptions import ObjectDoesNotExist


class CalendarByArtist(generics.RetrieveUpdateDestroyAPIView):

    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

    def get_object(self, pk=None):
        language = check_accept_language(self.request)
        if pk is None:
            pk = self.kwargs['pk']
        try:
            artist = Artist.objects.get(id=pk)
            calendar = Calendar.objects.get(portfolio_id=artist.portfolio.id)
            return calendar
        except Calendar.DoesNotExist:
            Assertions.assert_true_raise404(False,
                                            translate(language, 'ERROR_CALENDAR_NOT_FOUND'))
        except ObjectDoesNotExist:
            Assertions.assert_true_raise404(False,
                                            translate(language, 'ERROR_NO_ARTIST_FOUND'))

    def get(self, request, pk=None, format=None):
        if pk is None:
            pk = self.kwargs['pk']
        calendar = self.get_object(pk)
        serializer = CalendarSerializer(calendar)
        return Response(serializer.data)


class CalendarManager(generics.RetrieveUpdateDestroyAPIView):

    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

    def get_object(self, pk=None):
        language = check_accept_language(self.request)
        if pk is None:
            pk = self.kwargs['pk']
        try:
            return Calendar.objects.get(portfolio__artist__id=pk)
        except Calendar.DoesNotExist:
            Assertions.assert_true_raise404(False,
                                            translate(language, 'ERROR_CALENDAR_NOT_FOUND'))
        except ObjectDoesNotExist:
            Assertions.assert_true_raise404(False,
                                            translate(language, 'ERROR_NO_ARTIST_FOUND'))


    def get(self, request, pk=None, format=None):
        language = check_accept_language(request)
        if pk is None:
            pk = self.kwargs['pk']
        calendar = self.get_object(pk)
        Assertions.assert_true_raise404(calendar,
                                        translate(language, 'ERROR_CALENDAR_NOT_FOUND'))
        serializer = CalendarSerializer(calendar)
        return Response(serializer.data)

    def put(self, request, pk=None):
        language = check_accept_language(request)
        if pk is None:
            pk = self.kwargs['pk']
        calendar = self.get_object(pk)
        artist = Artist.objects.filter(pk=pk).first()
        if not calendar:
            calendar = Calendar.objects.create(days=[], portfolio=artist.portfolio)
            calendar.save(language)
        Assertions.assert_true_raise400(len(request.data) != 0, translate(language, 'ERROR_EMPTY_JSON'))
        Assertions.assert_true_raise404(calendar is not None,
                                        translate(language, 'ERROR_CALENDAR_NOT_FOUND'))

        loggedUser = get_logged_user(request)
        user_type = get_user_type(loggedUser)
        artist = Artist.objects.filter(portfolio=calendar.portfolio).first()
        Assertions.assert_true_raise403(user_type == 'Artist', translate(language, "ERROR_NOT_AN_ARTIST"))
        Assertions.assert_true_raise403(loggedUser is not None and loggedUser.id == artist.id, translate(language, 'ERROR_CALENDAR_NOT_THE_OWNER'))
        serializer = CalendarSerializer(calendar, data=request.data, partial=True)
        portfolio = loggedUser.portfolio.id
        print(portfolio)
        Assertions.assert_true_raise403(str(loggedUser.portfolio.id) == request.data['portfolio'], translate(language, 'ERROR_CALENDAR_NOT_THE_OWNER'))
        Assertions.assert_true_raise400(serializer.is_valid(), translate(language, 'ERROR_INVALID_DATA'))
        serializer.save(language, pk, loggedUser)

        return Response(status=status.HTTP_200_OK)

    def delete(self, request, pk=None, format=None):
        if pk is None:
            pk = self.kwargs['pk']

        language = check_accept_language(request)
        loggedUser = get_logged_user(request)
        user_type = get_user_type(loggedUser)

        calendar = self.get_object(pk)
        artist = Artist.objects.filter(portfolio=calendar.portfolio).first()
        Assertions.assert_true_raise403(loggedUser, translate(language, 'ERROR_NOT_LOGGED_IN'))
        Assertions.assert_true_raise403(user_type == 'Artist', translate(language, "ERROR_NOT_AN_ARTIST"))
        Assertions.assert_true_raise403(loggedUser is not None and loggedUser.id == artist.id, translate(language, 'ERROR_CALENDAR_NOT_THE_OWNER'))
        calendar = self.get_object(pk)
        calendar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateCalendar(generics.CreateAPIView):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

    def post(self, request, pk=None, **kwargs):
        language = check_accept_language(request)
        loggedUser = get_logged_user(request)
        type = get_user_type(loggedUser)
        Assertions.assert_true_raise403(loggedUser is not None and type == "Artist", translate(language, 'ERROR_NOT_AN_ARTIST'))
        serializer = CalendarSerializer(data=request.data, partial=True)
        portfolio = Portfolio.objects.filter(artist=loggedUser).first()
        if serializer.validate(request.data):
            serializer.is_valid()
            Assertions.assert_true_raise403(request.data["portfolio"] == portfolio.id, translate(language, 'ERROR_CALENDAR_NOT_THE_OWNER'))
            calendar = serializer.save(language, pk, loggedUser)
            serialized = CalendarSerializer(calendar)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
