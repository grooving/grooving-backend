from rest_framework import serializers
from rest_framework.exceptions import APIException


class Assertions:

    @staticmethod
    def assert_true_raise400(assertion: bool, details: dict):
        Assertions.__assert_true(assertion, 400, {"code": "invalid data"}, details)

    @staticmethod
    def assert_true_raise401(assertion: bool, details: dict = {"message": "No authenticate"} ):
        Assertions.__assert_true(assertion, 401, {"code": "No authenticate"}, details)

    @staticmethod
    def assert_true_raise403(assertion: bool, details: dict = {"code": "Denied persmission"}):
        Assertions.__assert_true(assertion, 403, {"code": "Denied persmission"}, details)

    @staticmethod
    def assert_true_raise404(assertion: bool):
        Assertions.__assert_true(assertion, 404, {"code": "Not Found"}, {"code": "Not Found"})

    @staticmethod
    def __assert_true(assertion: bool, http_error: int, code: dict , details: dict):
        if not assertion:
            print(code)
            print(details)
            exception = APIException(code=code, detail=details)
            exception.status_code = http_error
            raise exception


#Old functions - deprecated
def assert_true(boolean_value, message):
    if not boolean_value:
        print(message)
        raise serializers.ValidationError(message)
        # or ValueError(message) ? RestFramework views handle validationError exceptions



