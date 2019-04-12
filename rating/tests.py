from django.test import TestCase
from Grooving.models import Zone, User, Artist, Rating, EventLocation, Customer, Offer, Portfolio, PaymentPackage, Calendar, Performance
from datetime import datetime
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.contrib.auth.hashers import make_password


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

        offer1 = Offer.objects.create(description="DESCRIPTIONOFFER1", status='PAYMENT_MADE', date=date, price="200",
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
