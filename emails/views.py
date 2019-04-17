from utils.authentication_utils import get_admin
from rest_framework import generics
from utils.notifications.notifications import Notifications
from utils.Assertions import Assertions
from rest_framework.response import Response
from rest_framework import status
from emails.serializer import NotificationSerializer

# Create your views here.


class SendMailDataBreach(generics.CreateAPIView):
    serializer_class = NotificationSerializer

    def post(self, request, *args, **kwargs):                    # Indicamos que es un método HTTP GET
        admin = get_admin(request)
        subject = request.data.get("subject").strip()
        body = request.data.get("body").strip()

        Assertions.assert_true_raise403(admin, {"error": "You aren't an admin user"})
        Assertions.assert_true_raise400(subject, {'error': "Subject field not provided"})
        Assertions.assert_true_raise400(body, {'error': "Body field not provided"})

        Notifications.send_notification_for_breach_security(subject, body)

        return Response(status=status.HTTP_200_OK)

        # NotificationSerializer.send_mail(request)
        # NotificationSerializer(data=request.data)  Se usa a través del serializer (util cuando son muchos objetos)
        # Notifications.send_notification_for_breach_security()
