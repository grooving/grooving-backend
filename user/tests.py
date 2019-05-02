from rest_framework.test import APITransactionTestCase
from rest_framework import status
from Grooving.models import User, Admin, Artist, Customer
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase


class BanAndUnbanTestCase(APITransactionTestCase):

    def setUp(self):

        # Create an administrator

        user_admin = User.objects.create(username='admin', password=make_password('adminadmin'), is_staff=True,
                                           is_superuser=True, first_name='Chema', last_name='Alonso',
                                           email="admin@grooving.com")
        Token.objects.create(user=user_admin)
        user_admin.save()

        admin = Admin.objects.create(user=user_admin, language='es')
        admin.save()


        # Creating an artist

        user_artist = User.objects.create(username='artist1', password=make_password('artista1'),
                                            first_name='Carlos', last_name='Campos Cuesta',
                                            email="artist1fortest@gmail.com")
        Token.objects.create(user=user_artist)
        user_artist.save()

        artist = Artist.objects.create(user=user_artist, rating=4.5, phone='600304999',
                                        language='en',
                                        photo='https://upload.wikimedia.org/wikipedia/commons/e/e7/Robin_Clark_%28DJ%29_Live_at_Techno4ever_net_Bday_Rave.jpg',
                                        iban='ES6621000418401234567891',
                                        paypalAccount='artist1fortest@gmail.com')
        artist.save()

        user_artist2 = User.objects.create(username='artist2', password=make_password('artista2'),
                                            first_name='Carlos', last_name='Campos Cuesta',
                                            email="artist1fortest@gmail.com")
        Token.objects.create(user=user_artist2)
        user_artist2.save()

        artist2 = Artist.objects.create(user=user_artist2, rating=4.5, phone='600304999',
                                        language='en',
                                        photo='https://upload.wikimedia.org/wikipedia/commons/e/e7/Robin_Clark_%28DJ%29_Live_at_Techno4ever_net_Bday_Rave.jpg',
                                        iban='ES6621000418401234567891',
                                        paypalAccount='artist1fortest@gmail.com')
        artist2.save()

        # Creating a customer

        user_customer = User.objects.create(username='customer1', password=make_password('customer1customer1'),
                                               first_name='Rafael', last_name='Esquivias Ramírez',
                                               email="customer1fortest@gmail.com")
        Token.objects.create(user=user_customer)
        user_customer.save()

        customer = Customer.objects.create(user=user_customer, phone='639154189', holder='Rafael Esquivias Ramírez',
                                            expirationDate='2020-10-01', number='4651001401188232',
                                            language='en',
                                            paypalAccount="customer1fortest@gmail.com")
        customer.save()

    def generate_data(self, args):
        return {
            "id": args[1]
        }

    def test_driver_ban_unban_user(self):
        print("------------- Starting test -------------")

        admin = {"username": "admin", "password": "adminadmin"}
        response = self.client.post("/api/admin/login/", admin, format='json')

        token_num = response.get("x-auth")

        # Con esto evitamos problemas si el token no existe en bd

        token = ''

        try:
            token = Token.objects.all().filter(pk=token_num).first().key
        except:
            pass

        payload = [

            # Test positivo 1, banear un artista
            [token, 1, "es", status.HTTP_200_OK],

            # Test negativo 2, banear con Token None
            [None, 1, "es", status.HTTP_401_UNAUTHORIZED],

            # Test negativo 3: banear con Token vacío
            ["", 1, "es", status.HTTP_401_UNAUTHORIZED],

            # Test negativo 4: banear con Token inexistente
            ["dada21231d11", 1, "es", status.HTTP_401_UNAUTHORIZED],

            # Test positivo 5, banear un artista
            # [token, 2, "es", status.HTTP_200_OK],

            # Test negativo 6, banear con Token None
            # [None, 2, "es", status.HTTP_401_UNAUTHORIZED],

            # Test negativo 7: banear con Token vacío
            # ["", 2, "es", status.HTTP_401_UNAUTHORIZED],

            # Test negativo 8: banear con Token inexistente
            # ["dada21231d11", 2, "es", status.HTTP_401_UNAUTHORIZED],

        ]

        print("-------- Ban & unban testing --------")
        for data in payload:
            print("---> Test " + str(payload.index(data) + 1))
            self.template_ban_unban_user(data)

    def template_ban_unban_user(self, args):
        status_expected = args[-1]
        language = args[-2]

        data = self.generate_data(args)

        response = self.client.put("/user/", data, format="json",
                                   HTTP_AUTHORIZATION='Token ' + str(args[0]),
                                   HTTP_ACCEPT_LANGUAGE=language)

        self.assertEqual(status_expected, response.status_code)

        print("\nOk - Status expected: " + str(status_expected) + "\n")

'''
class UserTestCase(APITestCase):

    def test_signup_artist(self):

        data1={"first_name": "deffefeeffefe", "last_name": "david1", "password": "perroperro",
                "confirm_password": "perroperro", "username": "customer100", "email": "kiqo@gmail.com"}

        response = self.client.post("/signupArtist/",data1,format='json')
        self.assertEqual(response.status_code, 201)


    def test_signup_customer(self):

        data1={"first_name": "deffefeeffefe", "last_name": "david1", "password": "perroperro",
              "confirm_password": "perroperro", "username": "customer101", "email": "kiqo@gmail.com"}

        response = self.client.post("/signupCustomer/",data1,format='json')
        self.assertEqual(response.status_code, 201)
        
'''