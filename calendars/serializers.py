from django.contrib.auth.models import User, Group
from rest_framework import serializers
from Grooving.models import Calendar


class CalendarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Calendar
        fields = ('year', 'days')



