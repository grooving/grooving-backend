from utils.authentication_utils import get_admin
from rest_framework import generics
from utils.notifications.notifications import Notifications
from utils.Assertions import Assertions
from utils.authentication_utils import get_admin_2, get_logged_user
from rest_framework.response import Response
from rest_framework import status
from emails.serializer import NotificationSerializer
from emails.internationalization import translate


# Create your views here.


class SendMailDataBreach(generics.CreateAPIView):
    serializer_class = NotificationSerializer

    def post(self, request, *args, **kwargs):                    # Indicamos que es un método HTTP POST
        admin = get_admin_2(request)
        subject = request.data.get("subject")
        body = request.data.get("body")
        language = admin.language

        Assertions.assert_true_raise403(admin, translate(language, "ERROR_ADMIN_NOT_FOUND"))
        Assertions.assert_true_raise400(subject, translate(language, "ERROR_SUBJECT_NOT_PROVIDED"))
        Assertions.assert_true_raise400(body, translate(language, "ERROR_BODY_NOT_PROVIDED"))

        Notifications.send_notification_for_breach_security(subject, body)

        return Response(status=status.HTTP_200_OK)

        # NotificationSerializer.send_mail(request)
        # NotificationSerializer(data=request.data)  Se usa a través del serializer (util cuando son muchos objetos)
        # Notifications.send_notification_for_breach_security()


class DownloadPersonalData(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):
        artist_or_customer = get_logged_user(request)
        language = artist_or_customer.language

        Assertions.assert_true_raise403(artist_or_customer, translate(language, "ERROR_USER_NOT_FOUND"))
        Notifications.send_email_download_all_personal_data(artist_or_customer.user.id)

        return Response(status=status.HTTP_200_OK)
