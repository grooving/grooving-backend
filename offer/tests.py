from Grooving.models import Offer,  Artist, Portfolio, User, Calendar, PaymentPackage
from Grooving.models import EventLocation, Zone, Performance
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# Create your tests here.


class OfferTestCase(APITestCase):

    def test_accept_offer(self):

        days = [True] * 366

        user1_artist1 = User.objects.create(username='artist1', password=make_password('artist1artist1'),
                                            first_name='Cdds', last_name='Pedro',
                                            email='artist1@gmail.com')
        user1_artist1.save()

        zone1 = Zone.objects.create(name="Sevilla Sur")
        zone1.save()
        event_location1 = EventLocation.objects.create(name="Sala Rajoy", address="C/Madrid",
                                                       equipment="Speakers and microphone",
                                                       description="The best event location", zone=zone1)
        event_location1.save()

        portfolio1 = Portfolio.objects.create(artisticName="Juanartist")
        portfolio1.zone.add(zone1)
        portfolio1.save()

        artist1 = Artist.objects.create(user=user1_artist1, portfolio=portfolio1, phone='600304999')
        artist1.save()

        performance1 = Performance.objects.create(info="info", hours=3, price=200.0, currency="EUR")
        performance1.save()
        payment_package1 = PaymentPackage.objects.create(description="Paymentcription", appliedVAT="0.35",
                                                         portfolio=portfolio1, performance=performance1)

        payment_package1.save()

        calendar1 = Calendar.objects.create(year=2019, days=days, portfolio=portfolio1)
        calendar1.save()

        date = timezone.now()

        offer1 = Offer.objects.create(description="DESCRIPTIONOFFER1", status='PENDING', date=date, price="200",currency="EUR", hours=2,
                                      paymentCode='EEE', eventLocation=event_location1, paymentPackage=payment_package1)
        offer1.save()
        data1 = {"username": "artist1", "password": "artist1artist1"}
        response1 = self.client.post("/api/login/", data1, format='json')

        token = response1.find('x-auth')
        self.assertEqual(response1.status_code, 200)
        print(token)

        data = {"status": "CONTRACT_MADE"}
        response2 = self.client.put('/offer/1/', data, format='json')
        self.assertEqual(response2.status_code, 200)
        print(response2)
