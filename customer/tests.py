from django.test import TestCase
from rest_framework.authtoken.models import Token
from Grooving.models import Portfolio, Customer, Artist, Portfolio, User, Zone, EventLocation
from datetime import datetime
from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase
# Create your tests here.


class ShowCustomerInformation(TestCase):

    def test_show_personal_information_customer(self):
        user1_customer = User.objects.create(username='customer1', password=make_password('customer1'),
                                            first_name='Bunny', last_name='Fufuu',
                                            email='customer1@gmail.com')
        user1_customer.save()

        zone1 = Zone.objects.create(name="Sevilla Sur")
        zone1.save()

        customer1 = Customer.objects.create(user=user1_customer, holder="Juan", number='600304999', cvv=999,
                                            expirationDate=datetime.now())
        customer1.save()

        event_location1 = EventLocation.objects.create(name="Sala Rajoy", address="C/Madrid",
                                                       equipment="Speakers and microphone",
                                                       description="The best event location", zone=zone1,
                                                       customer=customer1)
        event_location1.save()

        data1 = {"username": "customer1", "password": "customer1"}
        response = self.client.post("/api/login/", data1, format='json')

        token_num = response.get('x-auth')
        token = Token.objects.all().filter(pk=token_num).first()
        self.assertEqual(response.status_code, 200)

        response2 = self.client.get('/customer/personalInformation/', format='json',
                                    HTTP_AUTHORIZATION='Token ' + token.key)
        self.assertEqual(response.status_code, 200)
        result = response2.json()

        item_dict = response2.json()
        #We check that only one user is retrieved
        self.assertTrue(len(item_dict) == 6)

        self.client.logout()

    def test_show_personal_information_artist_forbidden(self):
        user1_artist1 = User.objects.create(username='artist1', password=make_password('artist1'),
                                            first_name='Bunny', last_name='Fufuu',
                                            email='artist1@gmail.com')
        user1_artist1.save()

        zone1 = Zone.objects.create(name="Sevilla Sur")
        zone1.save()

        portfolio1 = Portfolio.objects.create(artisticName="Juanartist")
        portfolio1.zone.add(zone1)
        portfolio1.save()

        artist1 = Artist.objects.create(user=user1_artist1, portfolio=portfolio1, phone='600304999')
        artist1.save()

        data1 = {"username": "artist1", "password": "artist1"}
        response = self.client.post("/api/login/", data1, format='json')

        token_num = response.get('x-auth')
        token = Token.objects.all().filter(pk=token_num).first()

        self.assertEqual(response.status_code, 200)

        response2 = self.client.get('/customer/personalInformation/', format='json',
                                    HTTP_AUTHORIZATION='Token ' + token.key)

        self.assertEqual(response2.status_code, 403)
        self.client.logout()

    def test_show_personal_information_admin_forbidden(self):
        user1_artist1 = User.objects.create(username='artist1', password=make_password('artist1'),
                                            first_name='Bunny', last_name='Fufuu',
                                            email='artist1@gmail.com')
        user1_artist1.save()

        response2 = self.client.get('/customer/personalInformation/', format='json')
        self.assertEqual(response2.status_code, 403)
        self.client.logout()

    def test_show_personal_information_anonymous_forbidden(self):

        response = self.client.get('/customer/personalInformation/', format='json')
        self.assertEqual(response.status_code, 403)
