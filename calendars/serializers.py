from django.contrib.auth.models import User, Group
from rest_framework import serializers
from Grooving.models import Calendar, Portfolio
from utils.Assertions import assert_true, Assertions
import re
from utils.utils import check_accept_language
from .internationalization import translate


class CalendarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Calendar
        fields = ('days', 'portfolio')

    def save(self, language, pk=None, logged_user=None):
        if self.initial_data.get('id') is None and pk is None:
            # creation
            calendar = Calendar()
            calendar = self._service_create(self.initial_data, calendar, logged_user, language)
        else:
            # edit
            id = (self.initial_data, pk)[pk is not None]
            calendar = Calendar.objects.filter(portfolio_id=id).first()
            calendar = self._service_update(self.initial_data, calendar, logged_user, language)
        calendar.save()
        return calendar

    @staticmethod
    def _service_create(json: dict, calendar: Calendar, logged_user, language):

        Assertions.assert_true_raise403(logged_user is not None, translate(language, 'ERROR_NOT_LOGGED_IN'))

        portfolio = Portfolio.objects.filter(id=logged_user.portfolio.id).first()
        calendar = Calendar.objects.filter(portfolio=portfolio).first()

        Assertions.assert_true_raise400(calendar is None, translate(language, 'ERROR_CALENDAR_ALREADY_EXISTS'))

        calendar = Calendar()

        r = re.compile('\d{4}-\d{4}-\d{2}')
        Assertions.assert_true_raise400(json.get('days') is not None, translate(language, 'ERROR_NO_DAYS_GIVEN'))
        Assertions.assert_true_raise400(json.get('days') != '', translate(language, 'ERROR_NO_DAYS_GIVEN'))
        for day in json['days']:
            Assertions.assert_true_raise400(r.match(day), translate(language, 'ERROR_INCORRECT_FORMAT'))
            calendar.days.append(day)

        calendar.portfolio = portfolio
        calendar.save()

        return calendar

    @staticmethod
    def _service_update(json: dict, calendar: Calendar, logged_user: User, language):

        Assertions.assert_true_raise403(logged_user is not None, translate(language, 'ERROR_NOT_LOGGED_IN'))

        portfolio_in_db = Portfolio.objects.get(artist=logged_user)

        if not calendar.days:
            calendar.days = []
        Assertions.assert_true_raise400(portfolio_in_db.calendar == calendar, translate(language, 'ERROR_CALENDAR_NOT_THE_OWNER'))

        r = re.compile('^\d\d\d\d-(0?[1-9]|1[0-2])-(0?[1-9]|[12][0-9]|3[01])')
        Assertions.assert_true_raise400(json.get('days') is not None, translate(language, 'ERROR_NO_DAYS_GIVEN'))
        for day in json['days']:
            Assertions.assert_true_raise400(r.match(day), translate(language, 'ERROR_INCORRECT_FORMAT'))

        Assertions.assert_true_raise400(calendar is not None, translate(language, 'ERROR_CALENDAR_NOT_FOUND'))
        for db_day in calendar.days:
            aux = True
            for day in json['days']:
                if db_day == day:
                    aux = False
            if aux:
                calendar.days.remove(db_day)

        for day in json['days']:
            aux = True
            for db_day in calendar.days:
                if db_day == day:
                    aux = False
            if aux:
                calendar.days.append(day)

        return calendar