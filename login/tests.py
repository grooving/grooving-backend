from django.contrib.auth.hashers import make_password
from Grooving.models import User, Customer, Artist, Zone, Portfolio
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
import datetime, pytz

# Create your tests here.

class OfferTestCase(APITestCase):

    def test_login(self):
        print("TEST_LOGIN\n")

        # Populate database
        print("Populating database...\n")

        user1 = User.objects.create(username='artist1', password=make_password('artist1artist1'),
                                                  first_name='Cdds', last_name='Pedro',
                                                  email='artist1@gmail.com')
        user1.save()

        user2 = User.objects.create(username='customer1', password=make_password('customer1customer1'),
                                              first_name='Cdds', last_name='Pedro',
                                              email='customer1@gmail.com')
        user2.save()

        date = datetime.datetime(2020, 2, 7, 8, 49, 56, 81433, pytz.UTC)

        customer1 = Customer.objects.create(holder="customer1", expirationDate=date, user=user2,
                                            number=9393393939393, cvv=203)
        customer1.save()

        zone1 = Zone.objects.create(name="Sevilla Sur")
        zone1.save()

        portfolio1 = Portfolio.objects.create(artisticName="Juanartist")
        portfolio1.zone.add(zone1)
        portfolio1.save()

        artist1 = Artist.objects.create(user=user1, portfolio=portfolio1, phone='600304999')
        artist1.save()

        # Start test
        print("Launching test...\n")

        loginBody = {"username": "artist1", "password": "artist1artist1"}
        response = self.client.post("/api/login/", loginBody, format='json')
        self.assertEqual(response.status_code, 200)

        token_num = response.get('x-auth')
        token = Token.objects.all().filter(pk=token_num).first()
        print("--Token generated: " + token.key)
        print("--Artist login response: \n" + str(response.content) + "\n")

        loginBody = {"username": "customer1", "password": "customer1customer1"}
        response = self.client.post("/api/login/", loginBody, format='json')
        self.assertEqual(response.status_code, 200)

        token_num = response.get('x-auth')
        token = Token.objects.all().filter(pk=token_num).first()
        print("--Token generated: " + token.key)
        print("--Customer login response: \n" + str(response.content) + "\n")

        loginBody = {"username": "root", "password": "root"}
        response = self.client.post("/api/login/", loginBody, format='json')
        self.assertEqual(response.status_code, 400)

        self.assertEqual(response.get('x-auth'), None)
        print("--Expected bad request: \n" + str(response.content) + "\n")
