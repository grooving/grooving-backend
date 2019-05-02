from rest_framework.test import APITransactionTestCase
from rest_framework import status
from django.test import TestCase
from rest_framework.authtoken.models import Token
from Grooving.models import Portfolio, Customer, Artist, Portfolio, User, Zone, EventLocation
from datetime import datetime
from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase
# Create your tests here.


class RegisterTestCase(APITransactionTestCase):

    def generateData(self, args):
        return {
            "first_name": args[0],
            "last_name": args[1],
            "username": args[2],
            "password": args[3],
            "confirm_password": args[4],
            "email": args[5],
            "photo": args[6]
        }

    def test_driver_register_customer(self):
        print("------------- Starting test -------------")

        payload = [
            # Positive case 1: create a customer with spanish language
            ["David", "Romero Esparraga", "artist1", "elArtistaEspañol", "elArtistaEspañol", "utri2099@gmail.com",
             "http://www.google.com/image.png", "es", status.HTTP_201_CREATED],

            # Positive case 2: create a customer with english language
            ["Miguel", "Barahona Estevez", "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_201_CREATED],

            # Negative case 3: create a customer with existing mail
            ["Miguel", "Barahona Estevez", "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Negative case 4: create a customer with name set to None
            [None, "Barahona Estevez", "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Negative case 5: create a customer with empty name
            ["", "Barahona Estevez", "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Negative case 6: create a customer with name with numbers
            ["Poli111$car", "Barahona Estevez", "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Negative case 7, create a customer with last_name set to None
            ["Policarco", None, "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Negative case 8, create a customer with empty last_name
            ["Policarco", "", "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Negative case 9, create a customer with last_name set to string with special characters
            ["Policarco", "Mi123$", "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 10, create a customer with username set to None
            ["Policarco", "Mi123$", None, "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 11, create a customer with empty username
            ["Policarco", "Hernandez", "", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 12, create a customer with existing username
            ["Policarco", "Hernandez", "artist1", "elArtistaIngles", "elArtistaIngles", "utri28100@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 13, create a customer with password None
            ["Policarco", "Mi123$", "artist2", None, "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 14, create a customer with empty password
            ["Policarco", "Miguelin", "artist2", "", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 15, create a customer with password lower that 7 characters
            ["Policarco", "Miguelin", "artist2", "123456", "123456", "utri210dada0@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 16, create a customer with confirm_password set to None
            ["Policarco", "Miguelin", "artist2", "1234g6gt", None, "utri210dada0@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 17, create a customer with empty confirm_password
            ["Policarco", "Miguelin", "artist2", "1234g6gt", "", "utri210dada0@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 18, create a customer with distinct passwords
            ["Policarco", "Miguelin", "artist2", "1234g6gt", "fsdgsdfgsdfgs", "utri210dada0@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 19, create a customer with insecure passwords
            ["Policarco", "Miguelin", "artist2", "1234g6gt", "1234g6gt", "",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 20, create a customer with insecure passwords
            ["Policarco", "Miguelin", "artist2", "1234g6gt", "1234g6gt", "utri210dada0@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 21, create a customer with not valid mail
            ["Policarco", "Miguelin", "artist22", "12a4g6g1b3t", "12a4g6g1b3t", "holdasda",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 22, create a customer with not valid image
            ["Policarco", "Miguelin", "artist22", "12a4g6g1b3t", "12a4g6g1b3t", "utri210dada0@gmail.com",
             "http:/ /www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 23, create a customer with empty image
            ["Policarco", "Miguelin", "artist22", "12a4g6g1b3t", "12a4g6g1b3t", "utri210dada0@gmail.com",
             "h", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 24, create a customer with language set to None
            ["Policarco", "Miguelin", "artist22", "12a4g6g1b3t", "12a4g6g1b3t", "utri210dada0@gmail.com",
             "http://www.google.com/image.png", None, status.HTTP_400_BAD_REQUEST],

            # Negative test 25, create a customer with language with not supported language
            ["Policarco", "Miguelin", "artist22", "12a4g6g1b3t", "12a4g6g1b3t", "utri210dada0@gmail.com",
             "http:/ /www.google.com/image.png", "pt", status.HTTP_400_BAD_REQUEST],




            # Negative case 26: create a customer with existing mail
            ["Miguel", "Barahona Estevez", "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "es", status.HTTP_400_BAD_REQUEST],

            # Negative case 27: create a customer with name set to None
            [None, "Barahona Estevez", "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "es", status.HTTP_400_BAD_REQUEST],

            # Negative case 28: create a customer with empty name
            ["", "Barahona Estevez", "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "es", status.HTTP_400_BAD_REQUEST],

            # Negative case 29: create a customer with name with numbers
            ["Poli111$car", "Barahona Estevez", "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "es", status.HTTP_400_BAD_REQUEST],

            # Negative case 30, create a customer with last_name set to None
            ["Policarco", None, "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "es", status.HTTP_400_BAD_REQUEST],

            # Negative case 31, create a customer with empty last_name
            ["Policarco", "", "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "es", status.HTTP_400_BAD_REQUEST],

            # Negative case 32, create a customer with last_name set to string with special characters
            ["Policarco", "Mi123$", "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 33, create a customer with username set to None
            ["Policarco", "Mi123$", None, "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 34, create a customer with empty username
            ["Policarco", "Hernandez", "", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 35, create a customer with existing username
            ["Policarco", "Hernandez", "artist1", "elArtistaIngles", "elArtistaIngles", "utri28100@gmail.com",
             "http://www.google.com/image.png", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 36, create a customer with password None
            ["Policarco", "Mi123$", "artist2", None, "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 37, create a customer with empty password
            ["Policarco", "Miguelin", "artist2", "", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 38, create a customer with password lower that 7 characters
            ["Policarco", "Miguelin", "artist2", "123456", "123456", "utri210dada0@gmail.com",
             "http://www.google.com/image.png", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 39, create a customer with confirm_password set to None
            ["Policarco", "Miguelin", "artist2", "1234g6gt", None, "utri210dada0@gmail.com",
             "http://www.google.com/image.png", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 40, create a customer with empty confirm_password
            ["Policarco", "Miguelin", "artist2", "1234g6gt", "", "utri210dada0@gmail.com",
             "http://www.google.com/image.png", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 41, create a customer with distinct passwords
            ["Policarco", "Miguelin", "artist2", "1234g6gt", "fsdgsdfgsdfgs", "utri210dada0@gmail.com",
             "http://www.google.com/image.png", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 42, create a customer with insecure passwords
            ["Policarco", "Miguelin", "artist2", "1234g6gt", "1234g6gt", "",
             "http://www.google.com/image.png", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 43, create a customer with insecure passwords
            ["Policarco", "Miguelin", "artist2", "1234g6gt", "1234g6gt", "utri210dada0@gmail.com",
             "http://www.google.com/image.png", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 44, create a customer with not valid mail
            ["Policarco", "Miguelin", "artist22", "12a4g6g1b3t", "12a4g6g1b3t", "holdasda",
             "http://www.google.com/image.png", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 45, create a customer with not valid image
            ["Policarco", "Miguelin", "artist22", "12a4g6g1b3t", "12a4g6g1b3t", "utri210dada0@gmail.com",
             "http:/ /www.google.com/image.png", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 46, create a customer with empty image
            ["Policarco", "Miguelin", "artist22", "12a4g6g1b3t", "12a4g6g1b3t", "utri210dada0@gmail.com",
             "h", "es", status.HTTP_400_BAD_REQUEST],

        ]

        print("-------- Creating artist testing --------")
        for data in payload:
            # setup
            print("---> Test " + str(payload.index(data) + 1))
            self.template_register_user(data)
            # teardown

    def template_register_user(self, args):
        status_expected = args[-1]
        language = args[-2]

        data = self.generateData(args)

        response = self.client.post("/signupCustomer/", data, format="json", HTTP_ACCEPT_LANGUAGE=language)
        self.assertEqual(status_expected, response.status_code)

        print("\nOk - Status expected: " + str(status_expected) + "\n")



'''
class ShowCustomerInformation(TestCase):

    def test_show_personal_information_customer(self):
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
        self.assertTrue(len(item_dict) == 7)

        self.client.logout()

    def test_show_public_information_customer(self):
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

        response2 = self.client.get('/customer/publicInformation/'+str(customer1.id)+'/', format='json')
        self.assertEqual(response2.status_code, 200)

        item_dict = response2.json()
        #We check that only one user is retrieved
        self.assertTrue(len(item_dict) == 4)

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
'''