from rest_framework import serializers


def assert_true(boolean_value, message):
    if not boolean_value:
        print(message)
        raise serializers.ValidationError(message)
        # or ValueError(message) ? RestFramework views handle validationError exceptions

