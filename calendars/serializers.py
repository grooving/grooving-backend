from django.contrib.auth.models import User, Group
from rest_framework import serializers
from Grooving.models import Calendar, Portfolio
from utils.Assertions import assert_true, Assertions
import re


class CalendarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Calendar
        fields = ('days', 'portfolio')

    def save(self, pk=None, logged_user=None):
        if self.initial_data.get('id') is None and pk is None:
            # creation
            calendar = Calendar()
            calendar = self._service_create(self.initial_data, calendar, logged_user)
        else:
            # edit
            id = (self.initial_data, pk)[pk is not None]
            calendar = Calendar.objects.filter(portfolio_id=id).first()
            calendar = self._service_update(self.initial_data, calendar, logged_user)
        calendar.save()
        return calendar

    @staticmethod
    def _service_create(json: dict, calendar: Calendar, logged_user):

        Assertions.assert_true_raise403(logged_user is not None)

        portfolio = Portfolio.objects.filter(id=logged_user.portfolio.id).first()
        calendar = Calendar.objects.filter(portfolio=portfolio).first()

        Assertions.assert_true_raise400(calendar is None, {'error': 'A calendar already exist for this artist'})

        calendar = Calendar()

        r = re.compile('\d{4}-\d{4}-\d{2}')
        Assertions.assert_true_raise400(json.get('days') is not None, {'error': 'No days field was given'})
        for day in json['days']:
            Assertions.assert_true_raise400(r.match(day), {'error': 'Bad format. Correct format YYYY-MM-DD'})
            calendar.days.append(day)

        calendar.portfolio = portfolio
        calendar.save()

        return calendar

    @staticmethod
    def _service_update(json: dict, calendar: Calendar, logged_user: User):

        Assertions.assert_true_raise403(logged_user is not None, {'error':'Not logged in'})

        portfolio_in_db = Portfolio.objects.get(id=logged_user.portfolio.id)

        if not calendar.days:
            calendar.days = []
        Assertions.assert_true_raise400(portfolio_in_db.calendar == calendar, {'error': 'This calendar doesnt belong to this user'})

        r = re.compile('^\d\d\d\d-(0?[1-9]|1[0-2])-(0?[1-9]|[12][0-9]|3[01])')
        Assertions.assert_true_raise400(json.get('days') is not None, {'error': 'No days field was given'})
        for day in json['days']:
            Assertions.assert_true_raise400(r.match(day), {'error': 'Bad format. Correct format YYYY-MM-DD'})

        Assertions.assert_true_raise400(calendar is not None, {'error': 'Calendar doesn´t exist'})
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