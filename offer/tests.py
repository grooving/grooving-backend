from Grooving.models import Offer,  Artist, Portfolio, User, Calendar, PaymentPackage, Customer
from Grooving.models import EventLocation, Zone, Performance
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
import datetime
import pytz


class OfferTestCase(APITestCase):

    def test_manage_offer_artist(self):

        days = ['2019-06-02', '2019-08-02', '2019-10-15', '2019-11-02']
        date = datetime.datetime(2020,2,7,8,49,56,81433, pytz.UTC)

        user1_artist1 = User.objects.create(username='artist1', password=make_password('artist1artist1'),
                                            first_name='Cdds', last_name='Pedro',
                                            email='artist1@gmail.com')
        user1_artist1.save()

        user1_customer1 = User.objects.create(username='customer1', password=make_password('customer1customer1'),
                                              first_name='Cdds', last_name='Pedro',
                                              email='customer1@gmail.com')
        user1_customer1.save()
        zone1 = Zone.objects.create(name="Sevilla Sur")
        zone1.save()

        customer1 = Customer.objects.create(holder="customer1", expirationDate=date, user=user1_customer1,
                                            number=9393393939393, cvv=203)

        customer1.save()
        event_location1 = EventLocation.objects.create(name="Sala Rajoy", address="C/Madrid",
                                                       equipment="Speakers and microphone",
                                                       description="The best event location",
                                                       zone=zone1, customer_id=customer1.id)
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

        calendar1 = Calendar.objects.create(days=days, portfolio=portfolio1)
        calendar1.save()

        offer1 = Offer.objects.create(description="DESCRIPTIONOFFER1", status='PENDING', date=date, price="200",
                                      currency="EUR", hours=2, paymentCode='EEE', eventLocation=event_location1,
                                      paymentPackage=payment_package1)
        offer1.save()

        data1 = {"username": "artist1", "password": "artist1artist1"}
        response = self.client.post("/api/login/", data1, format='json')

        token_num = response.get('x-auth')
        token = Token.objects.all().filter(pk=token_num).first()
        print(token.key)
        self.assertEqual(response.status_code, 200)

        data = {"status": "CONTRACT_MADE"}

        response1 = self.client.put('/offer/{}/'.format(offer1.id), data, format='json',
                                    HTTP_AUTHORIZATION='Token '+token.key)
        self.assertEqual(response1.status_code, 200)
        print(response1)

        data1 = {"status": "CANCELED"}

        response2 = self.client.put('/offer/{}/'.format(offer1.id), data1, format='json',
                                    HTTP_AUTHORIZATION='Token ' + token.key)
        self.assertEqual(response2.status_code, 200)

        data2 = {"username": "customer1", "password": "customer1customer1"}
        response3 = self.client.post("/api/login/", data2, format='json')
        token_num2 = response3.get('x-auth')
        token2 = Token.objects.all().filter(pk=token_num2).first()
        self.assertEqual(response3.status_code, 200)
        offer1.status = "PENDING"
        offer1.save()
        print("\n\n")
        data3 = {"status": "WITHDRAWN"}

        response4 = self.client.put('/offer/{}/'.format(offer1.id), data3, format='json',
                                    HTTP_AUTHORIZATION='Token ' + token2.key)
        self.assertEqual(response4.status_code, 200)

        offer1.status = "CONTRACT_MADE"
        offer1.save()
        data4 = {"status": "CANCELED"}
        response5 = self.client.put('/offer/{}/'.format(offer1.id), data4, format='json',
                                    HTTP_AUTHORIZATION='Token ' + token2.key)
        self.assertEqual(response5.status_code, 200)

        offer1.status = "CONTRACT_MADE"
        offer1.save()

        response6 = self.client.get('/paymentCode/?offer={}'.format(offer1.id),
                                    HTTP_AUTHORIZATION='Token ' + token2.key)
        self.assertEqual(response6.status_code, 200)

        offer1.status = "CANCELED"
        offer1.save()

        response7 = self.client.get('/paymentCode/?offer={}'.format(offer1.id),
                                    HTTP_AUTHORIZATION='Token ' + token2.key)
        self.assertEqual(response7.status_code, 200)
        offer1.status = "PAYMENT_MADE"
        offer1.save()

        response8 = self.client.get('/paymentCode/?offer={}'.format(offer1.id),
                                    HTTP_AUTHORIZATION='Token ' + token2.key)
        self.assertEqual(response8.status_code, 200)

        offer1.status = "CONTRACT_MADE"
        offer1.save()
        data5 = {"paymentCode": "EEE"}
        response9 = self.client.put('/paymentCode/', data5, format='json',
                                    HTTP_AUTHORIZATION='Token ' + token.key)

        print(Offer.objects.filter(pk=offer1.id).first().status)
        self.assertEqual(response9.status_code, 200)


