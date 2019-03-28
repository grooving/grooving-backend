from django.contrib.auth.models import User, Group
from rest_framework import serializers
from Grooving.models import PortfolioModule


class PortfolioModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = PortfolioModule
        fields = ('type', 'link', 'description', 'portfolio')



