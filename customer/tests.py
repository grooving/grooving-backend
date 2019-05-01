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
            # Test positivo 1, crea un artista con language en español
            ["David", "Romero Esparraga", "artist1", "elArtistaEspañol", "elArtistaEspañol", "utri2099@gmail.com",
             "http://www.google.com/image.png", "es", status.HTTP_201_CREATED],

            # Test positivo 2, crea un artista con language en inglés
            ["Miguel", "Barahona Estevez", "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_201_CREATED],

            # Test positivo 3, crea un artista con un correo ya existente
            ["Miguel", "Barahona Estevez", "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Test positivo 4, crea un artista con el nombre None
            [None, "Barahona Estevez", "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Test negativo 5, crea un artista con el nombre vacío
            ["", "Barahona Estevez", "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Test negativo 6, crea un artista con el nombre con números y caracteres especiales
            ["Poli111$car", "Barahona Estevez", "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Test negativo 7, crea un artista con el apellido None
            ["Policarco", None, "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Test negativo 8, crea un artista con el apellido vacío
            ["Policarco", "", "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Test negativo 9, crea un artista con el apellido con números y caracteres
            ["Policarco", "Mi123$", "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Test negativo 10, crea un artista con username None
            ["Policarco", "Mi123$", None, "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Test negativo 11, crea un artista con username vacío
            ["Policarco", "Hernandez", "", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Test negativo 12, crea un artista con username ya existente
            ["Policarco", "Hernandez", "artist1", "elArtistaIngles", "elArtistaIngles", "utri28100@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Test negativo 13, crea un artista con password None
            ["Policarco", "Mi123$", "artist2", None, "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Test negativo 14, crea un artista con password vacía
            ["Policarco", "Miguelin", "artist2", "", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Test negativo 15, crea un artista con tamaño menor a 7 caracteres
            ["Policarco", "Miguelin", "artist2", "123456", "123456", "utri210dada0@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Test negativo 16, crea un artista con tamaño menor a 7 caracteres
            ["Policarco", "Miguelin", "artist2", "1234g6gt", None, "utri210dada0@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Test negativo 17, crea un artista con tamaño menor a 7 caracteres
            ["Policarco", "Miguelin", "artist2", "1234g6gt", "", "utri210dada0@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Test negativo 18, crea un artista con contraseñas que no coinciden
            ["Policarco", "Miguelin", "artist2", "1234g6gt", "fsdgsdfgsdfgs", "utri210dada0@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Test negativo 19, crea un artista con contraseñas poco seguras
            ["Policarco", "Miguelin", "artist2", "1234g6gt", "1234g6gt", "",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Test negativo 20, crea un artista con contraseñas poco seguras
            ["Policarco", "Miguelin", "artist2", "1234g6gt", "1234g6gt", "utri210dada0@gmail.com",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Test negativo 21, crea un artista con email no valido
            ["Policarco", "Miguelin", "artist22", "12a4g6g1b3t", "12a4g6g1b3t", "holdasda",
             "http://www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Test negativo 22, crea un artista con imagen no válida
            ["Policarco", "Miguelin", "artist22", "12a4g6g1b3t", "12a4g6g1b3t", "utri210dada0@gmail.com",
             "http:/ /www.google.com/image.png", "en", status.HTTP_400_BAD_REQUEST],

            # Test negativo 23, crea un artista con imagen vacío
            ["Policarco", "Miguelin", "artist22", "12a4g6g1b3t", "12a4g6g1b3t", "utri210dada0@gmail.com",
             "h", "El chungo de Torreblanca", "en", status.HTTP_400_BAD_REQUEST],

            # Test negativo 24, crea un artista con language None
            ["Policarco", "Miguelin", "artist22", "12a4g6g1b3t", "12a4g6g1b3t", "utri210dada0@gmail.com",
             "http://www.google.com/image.png", None, status.HTTP_400_BAD_REQUEST],

            # Test negativo 25, crea un artista con language no soportado
            ["Policarco", "Miguelin", "artist22", "12a4g6g1b3t", "12a4g6g1b3t", "utri210dada0@gmail.com",
             "http:/ /www.google.com/image.png", "pt", status.HTTP_400_BAD_REQUEST],

        ]

        print("-------- Creating artist testing --------")
        for data in payload:
            print("---> Test " + str(payload.index(data) + 1))
            self.template_register_user(data)

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