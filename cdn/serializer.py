from rest_framework import serializers

class UselessSerializer(serializers.Serializer):
    cosa= serializers.IntegerField(max_value=None, min_value=None)