'''from django.contrib.auth.hashers import make_password
from Grooving.models import Offer, Customer, Artist, Portfolio, User, Calendar, PaymentPackage, EventLocation, Zone, Performance
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
import datetime, pytz

# Create your tests here.

class EventLocationTest(APITestCase):

    def test_create_eventlocation_customer(self):
        print("TEST_CREATE_EVENTLOCATIO_CUSTOMER\n")

        # Populate database
        print("Populating database...\n")

        user2 = User.objects.create(username='customer1', password=make_password('customer1customer1'),
                                    first_name='Cdds', last_name='Pedro',
                                    email='customer1@gmail.com')
        user2.save()

        date = datetime.datetime(2020, 2, 7, 8, 49, 56, 81433, pytz.UTC)

        customer1 = Customer.objects.create(holder="customer1", expirationDate=date, user=user2,
                                            number=9393393939393, cvv=203)
        customer1.save()

        zone1 = Zone.objects.create(name="Sevilla")
        zone1.save()
        zone2 = Zone.objects.create(name="Sevilla Este", parentZone=zone1)
        zone2.save()

        # Start test
        print("Launching test...\n")

        loginBody = {"username": "customer1", "password": "customer1customer1"}
        response = self.client.post("/api/login/", loginBody, format='json')
        self.assertEqual(response.status_code, 200)

        token_num = response.get('x-auth')
        token = Token.objects.all().filter(pk=token_num).first()
        print("--Token generated: " + token.key)

        body = {
            "address": "Calle Ecija",
            "zone_id": zone2.id
        }

        response = self.client.post('/eventlocation/', body, format='json',
                                                    HTTP_AUTHORIZATION='Token ' + token.key)
        self.assertEqual(response.status_code, 201)
        print("--Event location created:\n" + str(response.content))

        body = {
            "address": "Calle Ecija",
            "zone_id": zone1.id
        }

        response = self.client.post('/eventlocation/', body, format='json',
                                    HTTP_AUTHORIZATION='Token ' + token.key)
        self.assertEqual(response.status_code, 400)
        print("--Event location didn't created:\n" + str(response.content))

        body = {
            "zone_id": zone1.id
        }

        response = self.client.post('/eventlocation/', body, format='json',
                                    HTTP_AUTHORIZATION='Token ' + token.key)
        self.assertEqual(response.status_code, 400)
        print("--Bad request expected:\n" + str(response.content))

        response = self.client.post('/eventlocation/', body, format='json')

        self.assertEqual(response.status_code, 401)
        print("--User non authenticated:\n" + str(response.content))

        print("\nPASSED\n")'''
