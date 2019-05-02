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

            # Positive test 1, ban artist
            [token, 2, "es", status.HTTP_200_OK],

            # Positive test 2, unban artist
            [token, 2, "es", status.HTTP_200_OK],

            # Negative test 3, ban artist with token None
            [None, 2, "es", status.HTTP_401_UNAUTHORIZED],

            # Negative test 4: ban artist with empty Token
            ["", 2, "es", status.HTTP_401_UNAUTHORIZED],

            # Negative test 5: ban artist with token that not exists
            ["dada21231d11", 2, "es", status.HTTP_401_UNAUTHORIZED],

            # Positive test 6, ban customer
            [token, 3, "es", status.HTTP_200_OK],

            # Positive test 7, unban customer
            [token, 3, "es", status.HTTP_200_OK],

            # Negative test 8, ban customer with token None
            [None, 3, "es", status.HTTP_401_UNAUTHORIZED],

            # Negative test 9: ban customer with empty Token
            ["", 3, "es", status.HTTP_401_UNAUTHORIZED],

            # Negative test 10: ban customer with Token that not exist
            ["dada21231d11", 3, "es", status.HTTP_401_UNAUTHORIZED],

            # Negative test 11: ban user with user_id None
            [token, None, "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 12: ban user with user_id like string
            [token, "", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 13: ban user with user_id that not exists
            [token, 564, "es", status.HTTP_400_BAD_REQUEST],

            # Positive test 14, ban artist
            [token, 2, "en", status.HTTP_200_OK],

            # Positive test 15, unban artist
            [token, 2, "en", status.HTTP_200_OK],

            # Negative test 16, ban artist with token None
            [None, 2, "en", status.HTTP_401_UNAUTHORIZED],

            # Negative test 17: ban artist with empty Token
            ["", 2, "en", status.HTTP_401_UNAUTHORIZED],

            # Negative test 18: ban artist with token that not exists
            ["dada21231d11", 2, "en", status.HTTP_401_UNAUTHORIZED],

            # Positive test 19, ban customer
            [token, 3, "en", status.HTTP_200_OK],

            # Positive test 20, unban customer
            [token, 3, "en", status.HTTP_200_OK],

            # Negative test 21, ban customer with token None
            [None, 3, "en", status.HTTP_401_UNAUTHORIZED],

            # Negative test 22: ban customer with empty Token
            ["", 3, "en", status.HTTP_401_UNAUTHORIZED],

            # Negative test 23: ban customer with Token that not exist
            ["dada21231d11", 3, "en", status.HTTP_401_UNAUTHORIZED],

            # Negative test 24: ban user with user_id None
            [token, None, "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 25: ban user with user_id like string
            [token, "", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 26: ban user with user_id that not exists
            [token, 564, "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 27: ban user with language like integer
            [token, 3, 1, status.HTTP_400_BAD_REQUEST],

            # Negative test 28: ban user with lenguage set to None
            [token, 3, None, status.HTTP_400_BAD_REQUEST],

            # Negative test 29: ban user with empty language
            [token, 3, "", status.HTTP_400_BAD_REQUEST],

            # Negative test 30: ban user with language that not exists
            [token, 3, "pt", status.HTTP_400_BAD_REQUEST],

            # Negative test 31: ban user with lenguage set to None
            [token, 2, None, status.HTTP_400_BAD_REQUEST],
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
