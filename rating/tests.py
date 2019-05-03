from django.test import TestCase
from Grooving.models import Zone, User, Artist, Rating, EventLocation, Customer, Offer, Portfolio, PaymentPackage, Calendar, Custom
from datetime import datetime
from rest_framework.authtoken.models import Token
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

        user2_artist1 = User.objects.create(username='artis)t1', password=make_password('artist1'),
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
            #self.template_rate_offer(data, "en")
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

"""
class RatingTestCase(TestCase):

    def test_create_rating_not_a_customer(self):
        user1_customer = User.objects.create(username='customer1', password=make_password('customer1'),
                                             first_name='Bunny', last_name='Fufuu',
                                             email='customer1@gmail.com')
        user1_customer.save()

        user_admin = User.objects.create(username='admin', password=make_password('admin'),
                                             first_name='Bunny', last_name='Fufuu',
                                             email='admin1@gmail.com', is_staff=True)
        user_admin.save()

        zone1 = Zone.objects.create(name="Sevilla Sur")
        zone1.save()

        customer1 = Customer.objects.create(user=user1_customer, holder="Juan", number='600304999',
                                            expirationDate=datetime.now())
        customer1.save()

        event_location1 = EventLocation.objects.create(name="Sala Rajoy", address="C/Madrid",
                                                       equipment="Speakers and microphone",
                                                       description="The best event location", zone=zone1,
                                                       customer=customer1)
        event_location1.save()

        days = ['2019-06-02', '2019-08-02']

        user2_artist1 = User.objects.create(username='artist1', password=make_password('artist1'),
                                            first_name='Bunny', last_name='Cucuu',
                                            email='artist1@gmail.com')
        user2_artist1.save()

        zone1 = Zone.objects.create(name="Sevilla Sur")
        zone1.save()

        portfolio1 = Portfolio.objects.create(artisticName="Juanartist")
        portfolio1.zone.add(zone1)
        portfolio1.save()

        artist1 = Artist.objects.create(user=user2_artist1, portfolio=portfolio1, phone='600304999')
        artist1.save()

        calendar1 = Calendar.objects.create(days=days, portfolio=portfolio1)
        calendar1.save()

        performance1 = Performance.objects.create(info="info", hours=3, price=200.0)
        performance1.save()
        payment_package1 = PaymentPackage.objects.create(description="Paymentcription",
                                                         portfolio=portfolio1, performance=performance1)

        payment_package1.save()

        date = timezone.now()

        offer1 = Offer.objects.create(description="DESCRIPTIONOFFER1", status='PAYMENT_MADE', date=timezone.now(), price="200",
                                      currency="EUR", hours=2, appliedVAT="0.35",
                                      paymentCode='EEE', eventLocation=event_location1, paymentPackage=payment_package1)
        offer1.save()

        responseAnon = self.client.post('/customer/rating/{}/'.format(offer1.id), format='json')

        self.assertEqual(responseAnon.status_code, 403)

        data1 = {"username": "artist1", "password": "artist1"}
        response = self.client.post("/api/login/", data1, format='json')

        token_num = response.get('x-auth')
        token = Token.objects.all().filter(pk=token_num).first()

        self.assertEqual(response.status_code, 200)

        response2 = self.client.post('/customer/rating/{}/'.format(offer1.id), format='json',
                                                                HTTP_AUTHORIZATION='Token ' + token.key)
        self.assertEqual(response2.status_code, 403)

        self.client.logout()

        #rating = Rating.objects.create(score=5, comment="Lo ha hecho explendido")

        #response2 = self.client.post('/customer/rating/{}/'.format(offer1.id), data2, format='json',
        #                            HTTP_AUTHORIZATION='Token ' + token.key)
        #self.assertEqual(response2.status_code, 200)


    def test_create_rating_invalid_offer(self):
        user1_customer = User.objects.create(username='customer1', password=make_password('customer1'),
                                             first_name='Bunny', last_name='Fufuu',
                                             email='customer1@gmail.com')
        user1_customer.save()

        user1_customer2 = User.objects.create(username='customer2', password=make_password('customer2'),
                                             first_name='Bunny', last_name='Fufuu',
                                             email='customer1@gmail.com')
        user1_customer2.save()

        zone1 = Zone.objects.create(name="Sevilla Sur")
        zone1.save()

        customer1 = Customer.objects.create(user=user1_customer, holder="Juan", number='600304999',
                                            expirationDate=datetime.now())
        customer1.save()

        customer2 = Customer.objects.create(user=user1_customer2, holder="Juan", number='600304999',
                                            expirationDate=datetime.now())
        customer2.save()

        event_location1 = EventLocation.objects.create(name="Sala Rajoy", address="C/Madrid",
                                                       equipment="Speakers and microphone",
                                                       description="The best event location", zone=zone1,
                                                       customer=customer1)
        event_location1.save()

        days = ['2019-06-02', '2019-08-02']

        user2_artist1 = User.objects.create(username='artist1', password=make_password('artist1'),
                                            first_name='Bunny', last_name='Cucuu',
                                            email='artist1@gmail.com')
        user2_artist1.save()

        zone1 = Zone.objects.create(name="Sevilla Sur")
        zone1.save()

        portfolio1 = Portfolio.objects.create(artisticName="Juanartist")
        portfolio1.zone.add(zone1)
        portfolio1.save()

        artist1 = Artist.objects.create(user=user2_artist1, portfolio=portfolio1, phone='600304999')
        artist1.save()

        calendar1 = Calendar.objects.create(days=days, portfolio=portfolio1)
        calendar1.save()

        performance1 = Performance.objects.create(info="info", hours=3, price=200.0)
        performance1.save()
        payment_package1 = PaymentPackage.objects.create(description="Paymentcription",
                                                         portfolio=portfolio1, performance=performance1)

        payment_package1.save()

        date = timezone.now()

        offer1 = Offer.objects.create(description="DESCRIPTIONOFFER1", status='PENDING', date=date, price="200",
                                      currency="EUR", hours=2, appliedVAT="0.35",
                                      paymentCode='EEE', eventLocation=event_location1, paymentPackage=payment_package1)
        offer1.save()

        rating = Rating.objects.create(score=5, comment="Lo ha hecho explendido")

        rating.save()

        offer2 = Offer.objects.create(description="DESCRIPTIONOFFER2", status='PAYMENT_MADE', date=date, price="200",
                                      currency="EUR", hours=3, appliedVAT="0.35",
                                      paymentCode='EEEE', eventLocation=event_location1, paymentPackage=payment_package1,
                                      rating=rating)
        offer2.save()

        data1 = {"username": "customer2", "password": "customer2"}
        response = self.client.post("/api/login/", data1, format='json')

        token_num = response.get('x-auth')
        token = Token.objects.all().filter(pk=token_num).first()

        self.assertEqual(response.status_code, 200)

        #Login with the wrong customer

        response2 = self.client.post('/customer/rating/{}/'.format(offer1.id), format='json',
                                                                HTTP_AUTHORIZATION='Token ' + token.key)
        self.assertEqual(response2.status_code, 403)

        data1 = {"username": "customer1", "password": "customer1"}
        response = self.client.post("/api/login/", data1, format='json')

        token_num = response.get('x-auth')
        token = Token.objects.all().filter(pk=token_num).first()

        self.assertEqual(response.status_code, 200)

        #The offer isn't ready to receive a rating because it isn't in PAYMENT_MADE status

        response3 = self.client.post('/customer/rating/{}/'.format(offer1.id), format='json',
                                     HTTP_AUTHORIZATION='Token ' + token.key)
        self.assertEqual(response3.status_code, 401)

        #rating an offer which already has a rating

        response4 = self.client.post('/customer/rating/{}/'.format(offer2.id), format='json',
                                     HTTP_AUTHORIZATION='Token ' + token.key)
        self.assertEqual(response4.status_code, 401)

        self.client.logout()
"""
