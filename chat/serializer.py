from rest_framework import serializers
from Grooving.models import Chat
class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ("json")
