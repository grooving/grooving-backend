from Grooving.models import Zone, User, Artist, EventLocation, Customer, Offer, Portfolio, PaymentPackage, Calendar, Custom
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from rest_framework.test import APITransactionTestCase


class RatingTestCase(APITransactionTestCase):
    offerId ={"es": None, "en": None}
    artistId = None

    def setUp(self):
        user1_customer = User.objects.create(username='customer1', password=make_password('customer1'),
                                             first_name='Pepe', last_name='Pepez',
                                             email='customer1@isamail.com')

        user1_customer.save()

        customer1 = Customer.objects.create(user=user1_customer, holder="Pepe", number='600304999',
                                            expirationDate=datetime.now())
        customer1.save()

        zone1 = Zone.objects.create(name="Hispalis")
        zone1.save()
        event_location1 = EventLocation.objects.create(name="Sala Chope", address="C/Madrid",
                                                       equipment="Speakers and microphone",
                                                       description="The worst event location", zone=zone1,
                                                       customer=customer1)
        event_location1.save()

        user2_artist1 = User.objects.create(username='artist1', password=make_password('artist1'),
                                            first_name='Manolo', last_name='Manolez',
                                            email='artist1@isamail.com')
        user2_artist1.save()

        artist1 = Artist.objects.create(user=user2_artist1)
        artist1.save()
        self.artistId = artist1.pk

        portfolio1 = Portfolio.objects.create(artisticName="Manolo el Guitarras", artist=artist1)
        portfolio1.zone.add(zone1)
        portfolio1.save()
        days = ['2019-06-02', '2019-08-02']
        calendar1 = Calendar.objects.create(days=days, portfolio=portfolio1)
        calendar1.save()
        custom1 = Custom.objects.create(minimumPrice=100.0)
        custom1.save()

        package1 = PaymentPackage.objects.create(description="Yo toco la guitarra", portfolio=portfolio1, custom=custom1)
        package1.save()

        offer1 = Offer.objects.create(description="Una oferta sin igual", status='PAYMENT_MADE', date=timezone.now(),
                                      price=200.0,
                                      hours=2, appliedVAT=0.1,
                                      paymentCode="YeheaBoeh1", eventLocation=event_location1, paymentPackage=package1)
        offer1.save()

        self.offerId["es"] = offer1.pk

        offer2 = Offer.objects.create(description="Una oferta sin igual, V2", status='PAYMENT_MADE', date=timezone.now(),
                                      price=200.0,
                                      hours=2, appliedVAT=0.1,
                                      paymentCode="YeheaBoeh2", eventLocation=event_location1, paymentPackage=package1)
        offer2.save()

        self.offerId["en"] = offer2.pk

        user2_customer = User.objects.create(username='customer2', password=make_password('customer2'),
                                             first_name='Yeah', last_name='Pepez',
                                             email='customer2@isamail.com')

        user2_customer.save()

        customer2 = Customer.objects.create(user=user2_customer, holder="Pepe", number='600304799',
                                            expirationDate=datetime.now())
        customer2.save()

        event_location2 = EventLocation.objects.create(name="Sala Chope", address="C/Madrid",
                                                       equipment="Speakers and microphone",
                                                       description="The worst event location", zone=zone1,
                                                       customer=customer2)
        event_location2.save()

    def test_driver_rate_offer(self):

        payload = [
            [None, "Yehea", "customer1", "customer1", 401],
            [-4, "Yehea", "customer1", "customer1", 401],
            [6, "Yehea", "customer1", "customer1", 401],
            [4.5, "Yehea", "customer1", "customer1", 401],
            [2, "Yehea", "artist1", "artist1", 403],
            [None, None, "artist1", "artist1", 403],
            [2, "Yehea", "customer2", "customer2", 403],
            [2, "Yehea", "customer1", "customer1", 201],
        ]

        indice = 1
        for data in payload:
            print("---> Test " + str(indice) + " es")
            self.template_rate_offer(data, "es")
            print("---> Test " + str(indice) + " en")
            self.template_rate_offer(data, "en")
            indice += 1


    def generate_data(self, args):
        return {
            "score": args[0],
            "comment": args[1]
        }

    def template_rate_offer(self, arg, lang):
        http_code = arg[-1]
        data = self.generate_data(arg)
        user = {"username": arg[2], "password": arg[3]}
        response = self.client.post("/api/login/", user, format='json')

        token_num = response.get("x-auth")

        response = self.client.post("/customer/rating/"+str(self.offerId.get(lang))+"/", data, format="json",
                                   HTTP_AUTHORIZATION='Token ' + token_num,
                                   HTTP_ACCEPT_LANGUAGE=lang)
        response2 = self.client.get("/artist/ratings/"+str(self.artistId)+"/")
        self.assertEqual(http_code, response.status_code)
        print(response.status_code)
        if response.status_code == 201:
            self.assertEqual(200, response2.status_code)
            print(response2.status_code)