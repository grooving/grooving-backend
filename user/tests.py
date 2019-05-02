from rest_framework.test import APITransactionTestCase
from rest_framework import status
from Grooving.models import User, Admin, Artist, Customer, Portfolio, Zone, EventLocation, Chat
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password


class BanAndUnbanTestCase(APITransactionTestCase):
    sharedData = {
    }

    def setUp(self):

        # Create an administrator

        user_admin = User.objects.create(username='admin', password=make_password('adminadmin'), is_staff=True,
                                         is_superuser=True, first_name='Chema', last_name='Alonso',
                                         email="admin@grooving.com")
        Token.objects.create(user=user_admin)
        user_admin.save()

        admin = Admin.objects.create(user=user_admin, language='es')
        admin.save()

        self.sharedData["admin_id"] = admin.id
        self.sharedData["admin_user_id"] = admin.id

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

        self.sharedData["artist_id"] = artist.id
        self.sharedData["artist_user_id"] = user_artist.id

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

        self.sharedData["customer_id"] = customer.id
        self.sharedData["customer_user_id"] = user_customer.id

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
            [token, self.sharedData["artist_user_id"], "es", status.HTTP_200_OK],

            # Positive test 2, unban artist
            [token, self.sharedData["artist_user_id"], "es", status.HTTP_200_OK],

            # Negative test 3, ban artist with token None
            [None, self.sharedData["artist_user_id"], "es", status.HTTP_401_UNAUTHORIZED],

            # Negative test 4: ban artist with empty Token
            ["", self.sharedData["artist_user_id"], "es", status.HTTP_401_UNAUTHORIZED],

            # Negative test 5: ban artist with token that not exists
            ["dada21231d11", self.sharedData["artist_user_id"], "es", status.HTTP_401_UNAUTHORIZED],

            # Positive test 6, ban customer
            [token, self.sharedData["customer_user_id"], "es", status.HTTP_200_OK],

            # Positive test 7, unban customer
            [token, self.sharedData["customer_user_id"], "es", status.HTTP_200_OK],

            # Negative test 8, ban customer with token None
            [None, self.sharedData["customer_user_id"], "es", status.HTTP_401_UNAUTHORIZED],

            # Negative test 9: ban customer with empty Token
            ["", self.sharedData["customer_user_id"], "es", status.HTTP_401_UNAUTHORIZED],

            # Negative test 10: ban customer with Token that not exist
            ["dada21231d11", self.sharedData["customer_user_id"], "es", status.HTTP_401_UNAUTHORIZED],

            # Negative test 11: ban user with user_id None
            [token, None, "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 12: ban user with user_id like string
            [token, "", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 13: ban user with user_id that not exists
            [token, 564, "es", status.HTTP_400_BAD_REQUEST],

            # Positive test 14, ban artist
            [token, self.sharedData["artist_user_id"], "en", status.HTTP_200_OK],

            # Positive test 15, unban artist
            [token, self.sharedData["artist_user_id"], "en", status.HTTP_200_OK],

            # Negative test 16, ban artist with token None
            [None, self.sharedData["artist_user_id"], "en", status.HTTP_401_UNAUTHORIZED],

            # Negative test 17: ban artist with empty Token
            ["", self.sharedData["artist_user_id"], "en", status.HTTP_401_UNAUTHORIZED],

            # Negative test 18: ban artist with token that not exists
            ["dada21231d11", self.sharedData["artist_user_id"], "en", status.HTTP_401_UNAUTHORIZED],

            # Positive test 19, ban customer
            [token, self.sharedData["customer_user_id"], "en", status.HTTP_200_OK],

            # Positive test 20, unban customer
            [token, self.sharedData["customer_user_id"], "en", status.HTTP_200_OK],

            # Negative test 21, ban customer with token None
            [None, self.sharedData["customer_user_id"], "en", status.HTTP_401_UNAUTHORIZED],

            # Negative test 22: ban customer with empty Token
            ["", self.sharedData["customer_user_id"], "en", status.HTTP_401_UNAUTHORIZED],

            # Negative test 23: ban customer with Token that not exist
            ["dada21231d11", self.sharedData["customer_user_id"], "en", status.HTTP_401_UNAUTHORIZED],

            # Negative test 24: ban user with user_id None
            [token, None, "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 25: ban user with user_id like string
            [token, "", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 26: ban user with user_id that not exists
            [token, 564, "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 27: ban user with language like integer
            [token, self.sharedData["customer_user_id"], 1, status.HTTP_400_BAD_REQUEST],

            # Negative test 28: ban user with lenguage set to None
            [token, self.sharedData["customer_user_id"], None, status.HTTP_400_BAD_REQUEST],

            # Negative test 29: ban user with empty language
            [token, self.sharedData["customer_user_id"], "", status.HTTP_400_BAD_REQUEST],

            # Negative test 30: ban user with language that not exists
            [token, self.sharedData["customer_user_id"], "pt", status.HTTP_400_BAD_REQUEST],
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


class RightToBeForgottenUserTestCase(APITransactionTestCase):

    sharedData = {
    }

    def generate_data(self, args):
        return {
            "id": args[1]  # user_id
        }

    def setUp(self):
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

        self.sharedData["artist_id"] = artist.id
        self.sharedData["artist_user_id"] = user_artist.id

        portfolio = Portfolio.objects.create(artisticName='Tamta',
                                             artist=artist,
                                             banner='http://www.ddi.com.au/wp-content/uploads/AdobeStock_115567415.jpeg',
                                             biography='Tamta, is a Georgian-Greek singer. She first achieved popularity in Greece and Cyprus in 2004 for her participation in Super Idol Greece, in which she placed second. She went on to release several charting albums and singles in Greece and Cyprus. Goduadze became a mentor on X Factor Georgia in 2014, and The X Factor Greece in 2016.')
        portfolio.save()

        # Creating a customer

        user_customer = User.objects.create(username='customer1', password=make_password('cliente1'),
                                            first_name='Rafael', last_name='Esquivias Ramírez',
                                            email="customer1fortest@gmail.com")
        Token.objects.create(user=user_customer)
        user_customer.save()

        customer = Customer.objects.create(user=user_customer, phone='639154189', holder='Rafael Esquivias Ramírez',
                                           expirationDate='2020-10-01', number='4651001401188232',
                                           language='en',
                                           paypalAccount="customer1fortest@gmail.com")
        customer.save()

        self.sharedData["customer_id"] = customer.id
        self.sharedData["customer_user_id"] = user_customer.id

        # Andalucía
        zone = Zone.objects.create(name='Sevilla')
        zone.save()

        event_location1 = EventLocation.objects.create(name='Event 1 - Festival Rockupo',
                                                       address='Universidad Pablo de Olavide', equipment='No',
                                                       zone=zone,
                                                       customer=customer)
        event_location1.save()

    def test_right_to_be_forgotten(self):
        print("------------- Starting test -------------")

        artist_data = {"username": "artist1", "password": "artista1"}
        response_artist = self.client.post("/api/login/", artist_data, format='json')

        customer_data = {"username": "customer1", "password": "cliente1"}
        response_customer = self.client.post("/api/login/", customer_data, format='json')

        token_num_artist = response_artist.get("x-auth")
        token_artist = Token.objects.all().filter(pk=token_num_artist).first().key
        token_num_customer = response_customer.get("x-auth")
        token_customer = Token.objects.all().filter(pk=token_num_customer).first().key

        payload = [
            # Negative test 1, forgotten user that Token is None
            [None, "es", status.HTTP_401_UNAUTHORIZED],

            # Negative test 2, forgotten user that Token doesn't exists
            ["d123dqwd", "es", status.HTTP_401_UNAUTHORIZED],

            # Negative test 3, forgotten user that Token is integer
            [1, "es", status.HTTP_401_UNAUTHORIZED],

            # Negative test 4, forgotten user that language set None
            [token_customer, None, status.HTTP_400_BAD_REQUEST],

            # Negative test 5, forgotten user that language doesn't exists
            [token_artist, "ds", status.HTTP_400_BAD_REQUEST],

            # Negative test 6, forgotten user that language set to integer
            [token_artist, 1, status.HTTP_400_BAD_REQUEST],

            # Positive test 7, forgotten artist
            [token_artist, "es", status.HTTP_204_NO_CONTENT],

            # Negative test 8, forgotten artist that has been deleted previously
            [token_artist, "es", status.HTTP_401_UNAUTHORIZED],

            # Positive test 9, forgotten customer
            [token_customer, "es", status.HTTP_204_NO_CONTENT],

            # Negative test 10, forgotten customer that has been deleted previously
            [token_customer, "es", status.HTTP_401_UNAUTHORIZED],
        ]

        print("-------- Right to be forgotten testing --------")

        indice = 1

        for data in payload:
            print("---> Test " + str(indice))
            self.template_right_to_be_forgotten(data)
            indice += 1

    def template_right_to_be_forgotten(self, args):
        status_expected = args[-1]
        language = args[-2]

        data = self.generate_data(args)

        response = self.client.delete("/user/", data, format="json",
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
