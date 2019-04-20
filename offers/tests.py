from django.test import TestCase

from Grooving.models import Offer, Customer, Artist, Portfolio, User, Calendar, PaymentPackage, EventLocation, Zone, Performance
from datetime import datetime
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase


class OfferTestCase(TestCase):

    def test_list_artist_offers(self):
        user1_customer = User.objects.create(username='customer1', password=make_password('customer1'),
                                             first_name='Bunny', last_name='Fufuu',
                                             email='customer1@gmail.com')
        user1_customer.save()

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
                                            first_name='Bunny', last_name='Fufuu',
                                            email='artist1@gmail.com')
        user2_artist1.save()

        zone1 = Zone.objects.create(name="Sevilla Sur")
        zone1.save()

        artist1 = Artist.objects.create(user=user2_artist1, phone='600304999')
        artist1.save()

        portfolio1 = Portfolio.objects.create(artisticName="Juanartist", artist=artist1)
        portfolio1.zone.add(zone1)
        portfolio1.save()

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

        #Second batch of data for the test

        user3_customer2 = User.objects.create(username='customer2', password=make_password('customer2'),
                                             first_name='Bunny', last_name='Fufuu',
                                             email='customer2@gmail.com')
        user3_customer2.save()

        zone2 = Zone.objects.create(name="Sevilla Sur")
        zone2.save()

        customer2 = Customer.objects.create(user=user3_customer2, holder="Juan", number='600304999',
                                            expirationDate=datetime.now())
        customer2.save()

        event_location2 = EventLocation.objects.create(name="Sala Rajoy", address="C/Madrid",
                                                       equipment="Speakers and microphone",
                                                       description="The best event location", zone=zone2,
                                                       customer=customer2)
        event_location2.save()

        user4_artist2 = User.objects.create(username='artist2', password=make_password('artist2'),
                                            first_name='Bunny', last_name='Fufuu',
                                            email='artist2@gmail.com')
        user4_artist2.save()

        artist2 = Artist.objects.create(user=user4_artist2, phone='600304999')
        artist2.save()

        portfolio2 = Portfolio.objects.create(artisticName="Juanartista", artist=artist2)
        portfolio2.zone.add(zone1)
        portfolio2.save()

        calendar2 = Calendar.objects.create(days=days, portfolio=portfolio2)
        calendar2.save()

        performance2 = Performance.objects.create(info="info", hours=3, price=200.0)
        performance2.save()
        payment_package2 = PaymentPackage.objects.create(description="Paymentcription",
                                                         portfolio=portfolio2, performance=performance2)

        payment_package2.save()

        offer2 = Offer.objects.create(description="DESCRIPTIONOFFER2", status='PENDING', date=date, price="200",
                                      currency="EUR", hours=2, appliedVAT="0.35",
                                      paymentCode='YUJU', eventLocation=event_location2, paymentPackage=payment_package2)
        offer2.save()

        data1 = {"username": "artist1", "password": "artist1"}
        response = self.client.post("/api/login/", data1, format='json')

        token_num = response.get('x-auth')
        token = Token.objects.all().filter(pk=token_num).first()

        self.assertEqual(response.status_code, 200)

        response2 = self.client.get('/artist/offers/', format='json', HTTP_AUTHORIZATION='Token '+token.key)
        self.assertEqual(response2.status_code, 200)
        item_dict = response2.json()

        self.assertTrue(len(item_dict['results']) == 1)
        self.client.logout()

    def test_list_customer_offers(self):

        user1_customer = User.objects.create(username='customer1', password=make_password('customer1'),
                                             first_name='Bunny', last_name='Fufuu',
                                             email='customer1@gmail.com')
        user1_customer.save()

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
                                            first_name='Bunny', last_name='Pato',
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

        # Second batch of data for the test

        user3_customer2 = User.objects.create(username='customer2', password=make_password('customer2'),
                                              first_name='Bunny', last_name='Fufuu',
                                              email='customer2@gmail.com')
        user3_customer2.save()

        zone2 = Zone.objects.create(name="Sevilla Sur")
        zone2.save()

        customer2 = Customer.objects.create(user=user3_customer2, holder="Juan", number='600304999',
                                            expirationDate=datetime.now())
        customer2.save()

        event_location2 = EventLocation.objects.create(name="Sala Rajoy", address="C/Madrid",
                                                       equipment="Speakers and microphone",
                                                       description="The best event location", zone=zone2,
                                                       customer=customer2)
        event_location2.save()



        user4_artist2 = User.objects.create(username='artist2', password=make_password('artist2'),
                                            first_name='Bunny', last_name='Fufuu',
                                            email='artist2@gmail.com')
        user4_artist2.save()

        portfolio2 = Portfolio.objects.create(artisticName="Juanito")
        portfolio2.zone.add(zone1)
        portfolio2.save()

        artist2 = Artist.objects.create(user=user4_artist2, portfolio=portfolio2, phone='600304999')
        artist2.save()

        calendar2 = Calendar.objects.create(days=days, portfolio=portfolio2)
        calendar2.save()

        performance2 = Performance.objects.create(info="info", hours=3, price=200.0)
        performance2.save()
        payment_package2 = PaymentPackage.objects.create(description="Paymentcription",
                                                         portfolio=portfolio2, performance=performance2)

        payment_package2.save()

        offer2 = Offer.objects.create(description="DESCRIPTIONOFFER2", status='PENDING', date=date, price="200",
                                      currency="EUR", hours=2,appliedVAT="0.35",
                                      paymentCode='YUJU', eventLocation=event_location1,
                                      paymentPackage=payment_package2)
        offer2.save()

        data1 = {"username": "customer1", "password": "customer1"}
        response = self.client.post("/api/login/", data1, format='json')

        token_num = response.get('x-auth')
        token = Token.objects.all().filter(pk=token_num).first()
        self.assertEqual(response.status_code, 200)

        response2 = self.client.get('/customer/offers/', format='json', HTTP_AUTHORIZATION='Token ' + token.key)
        self.assertEqual(response2.status_code, 200)
        item_dict = response2.json()
        self.assertTrue(len(item_dict['results']) == 2)
        self.client.logout()

    def test_list_no_offers(self):
        user1_customer = User.objects.create(username='customer1', password=make_password('customer1'),
                                             first_name='Bunny', last_name='Fufuu',
                                             email='customer1@gmail.com')
        user1_customer.save()

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
                                            first_name='Bunny', last_name='Fufuu',
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

        data1 = {"username": "artist1", "password": "artist1"}
        response = self.client.post("/api/login/", data1, format='json')

        token_num = response.get('x-auth')
        token = Token.objects.all().filter(pk=token_num).first()

        self.assertEqual(response.status_code, 200)

        response2 = self.client.get('/artist/offers/', format='json', HTTP_AUTHORIZATION='Token ' + token.key)
        self.assertEqual(response2.status_code, 200)
        item_dict = response2.json()

        self.assertTrue(len(item_dict['results']) == 0)


    def test_list_anonymous(self):

        response = self.client.get('/customer/offers/', format='json')
        self.assertEqual(response.status_code, 403)

    def test_list_admin(self):
        #admin user
        user3 = User()
        user3.username = "Manuel"
        user3.id = "17"
        user3.email = "fire@fire.com"
        user3.password = "Manuel"
        user3.is_staff = True
        user3.save()

        self.client.force_login(user3)
        response = self.client.get('/customer/offers/', format='json')
        self.assertEqual(response.status_code, 403)
        self.client.logout()
