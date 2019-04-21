from rest_framework import serializers
from utils.authentication_utils import get_admin
from utils.Assertions import Assertions
from utils.notifications.notifications import Notifications


class NotificationSerializer(serializers.Serializer):
    subject = serializers.CharField()
    body = serializers.CharField()

    @staticmethod
    def send_mail(request):

        Assertions.assert_true_raise403(get_admin(request) is not None, {"error": "You aren't an admin user"})

        body = request.data.get('body')
        subject = request.data.get('subject')

        # Assertions.assert_true_raise400(body and subject, {"error": "Body and subject is empty"})
        Assertions.assert_true_raise400(body, {"error": "Body is empty"})           # Salta si es None o cadena vacía
        Assertions.assert_true_raise400(subject, {"error": "Subject is empty"})     # Salta si es None o cadena vacía

        # Comprobar la cadena vacia

        Notifications.send_notification_for_breach_security(subject, body)
