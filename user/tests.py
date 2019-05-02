from rest_framework.test import APITransactionTestCase
from rest_framework import status
from Grooving.models import User, Admin, Artist, Customer
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password


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
            "id": args[1]  # user_id
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
            [token, 2, "es", status.HTTP_200_OK],

            # Test positivo 2, desbanear un artista
            [token, 2, "es", status.HTTP_200_OK],

            # Test negativo 3, banear un artista con Token None
            [None, 2, "es", status.HTTP_401_UNAUTHORIZED],

            # Test negativo 4: banear un artista con Token vacío
            ["", 2, "es", status.HTTP_401_UNAUTHORIZED],

            # Test negativo 5: banear un artista con Token inexistente
            ["dada21231d11", 2, "es", status.HTTP_401_UNAUTHORIZED],

            # Test negativo 6: banear un artista con lenguage a None
            [token, 2, None, status.HTTP_400_BAD_REQUEST],

            # Test negativo 7: banear un artista con lenguage vacío
            [token, 2, "", status.HTTP_400_BAD_REQUEST],

            # Test negativo 8: banear un artista con lenguage no existente
            [token, 2, "pt", status.HTTP_400_BAD_REQUEST],

            # Test positivo 9, banear un customer
            [token, 3, "es", status.HTTP_200_OK],

            # Test positivo 10, desbanear un customer
            [token, 3, "es", status.HTTP_200_OK],

            # Test negativo 11, banear un customer con Token None
            [None, 3, "es", status.HTTP_401_UNAUTHORIZED],

            # Test negativo 12: banear un customer con Token vacío
            ["", 3, "es", status.HTTP_401_UNAUTHORIZED],

            # Test negativo 13: banear un customer con Token inexistente
            ["dada21231d11", 3, "es", status.HTTP_401_UNAUTHORIZED],

            # Test negativo 14: banear un customer con lenguage a None
            [token, 3, None, status.HTTP_400_BAD_REQUEST],

            # Test negativo 15: banear un customer con lenguage vacío
            [token, 3, "", status.HTTP_400_BAD_REQUEST],

            # Test negativo 16: banear un customer con lenguage no existente
            [token, 3, "pt", status.HTTP_400_BAD_REQUEST],

            # Test negativo 17: banear un customer con lenguage como integer
            [token, 3, 1, status.HTTP_400_BAD_REQUEST],

            # Test negativo 18: banear un customer con user_id a None
            [token, None, "es", status.HTTP_400_BAD_REQUEST],

            # Test negativo 19: banear un customer con user_id como cadena
            [token, "", "es", status.HTTP_400_BAD_REQUEST],

            # Test negativo 20: banear un customer con user_id no existente
            [token, "1dasdads", "es", status.HTTP_400_BAD_REQUEST],
        ]

        print("-------- Ban & unban testing --------")

        indice = 1

        for data in payload:
            print("---> Test " + str(indice))
            self.template_ban_unban_user(data)
            indice += 1

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
