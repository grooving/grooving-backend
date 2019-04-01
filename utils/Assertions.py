from rest_framework import serializers
from rest_framework.exceptions import APIException


class Assertions:



    def assert_true_raise400():
    def assert_true_raise401():
    def assert_true_raise403():
    def assert_true_raise404():


    @staticmethod
    def __assert_true(assertion: bool, http_error: int, code: str, details: str):
        if not assertion:
            print(code)
            print(details)
            exception = APIException(code=code, details=details)
            exception.status_code = http_error
            raise exception


#Old functions - deprecated
def assert_true(boolean_value, message):
    if not boolean_value:
        print(message)
        raise serializers.ValidationError(message)
        # or ValueError(message) ? RestFramework views handle validationError exceptions



