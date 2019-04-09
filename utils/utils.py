from django.utils import timezone
from Grooving.models import SystemConfiguration
from rest_framework import generics
from rest_framework.response import Response


def auto_update_old_offers(offers):
    now = timezone.now()
    if not offers:
        pass
    if len(offers) == 0:
        pass
    else:
        for o in offers:
            if o.status == 'PENDING' and o.date < now:
                o.status = 'REJECTED'
                o.save()


class TermsAndConditions(generics.GenericAPIView):

    def get(self, request):
        return Response(SystemConfiguration.objects.all().first().termsText)
