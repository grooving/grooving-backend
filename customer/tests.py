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
            "photo": args[6],
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


class EditCustomerPersonalInformation(APITransactionTestCase):
    sharedData = {

    }

    def setUp(self):
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

        self.sharedData['customer_id'] = customer.id
        self.sharedData['user_customer_id'] = user_customer.id

    def generate_data(self, args):
        return {
            "first_name": args[1],
            "last_name": args[2],
            "phone": args[3],
            "photo": args[4],
            "username": args[5],
            "email": args[6]
        }

    def test_driver_edit_customer_personal_information(self):
        print("------------- Starting test -------------")

        customer = {"username": "customer1", "password": "cliente1"}
        response = self.client.post("/api/login/", customer, format='json')

        token_num = response.get("x-auth")

        # Con esto evitamos problemas si el token no existe en bd

        token = ''

        try:
            token = Token.objects.all().filter(pk=token_num).first().key
        except:
            pass

        payload = [
            # Positive test 1, edit customer personal information
            [token, "Juan Carlos", "Utrilla Martín", "666778899", "http://www.google.es/photo.png", customer["username"], "fakemailfortesting@gmail.com", "es",
             status.HTTP_200_OK],

            # Negative test 2, edit customer with token set None
            [None, "Juan Carlos", "Utrilla Martín", "666778899", "http://www.google.es/photo.png", customer["username"], "fakemailfortesting@gmail.com", "es",
             status.HTTP_401_UNAUTHORIZED],

            # Negative test 3, edit customer with token as integer
            [1, "Juan Carlos", "Utrilla Martín", "666778899", "http://www.google.es/photo.png", customer["username"], "fakemailfortesting@gmail.com", "es",
             status.HTTP_401_UNAUTHORIZED],

            # Negative test 4, edit customer with invalid token
            ["dasdaadas", "Juan Carlos", "Utrilla Martín", "666778899", "http://www.google.es/photo.png", customer["username"], "fakemailfortesting@gmail.com", "es",
             status.HTTP_401_UNAUTHORIZED],

            # Negative test 5, edit customer with first_name as None
            [token, None, "Utrilla Martín", "666778899", "http://www.google.es/photo.png", customer["username"], "fakemailfortesting@gmail.com", "es",
             status.HTTP_400_BAD_REQUEST],

            # Negative test 6, edit customer with first_name with special characters
            [token, "sdasd2123daadsad", "Utrilla Martín", "666778899", "http://www.google.es/photo.png", customer["username"], "fakemailfortesting@gmail.com", "es",
             status.HTTP_400_BAD_REQUEST],

            # Negative test 7, edit customer with first_name as integer
            [token, 1, "Utrilla Martín", "666778899", "http://www.google.es/photo.png", customer["username"], "fakemailfortesting@gmail.com", "es",
             status.HTTP_400_BAD_REQUEST],

            # Negative test 8, edit customer with last_name as None
            [token, "Juan Carlos", None, "666778899", "http://www.google.es/photo.png", customer["username"], "fakemailfortesting@gmail.com", "es",
             status.HTTP_400_BAD_REQUEST],

            # Negative test 9, edit customer with last_name with special characters
            [token, "Juan Carlos", "hfdsfsdfs23123sdas", "666778899", "http://www.google.es/photo.png", customer["username"], "fakemailfortesting@gmail.com", "es",
             status.HTTP_400_BAD_REQUEST],

            # Negative test 10, edit customer with last_name as integer
            [token, "Juan Carlos", 1, "666778899", "http://www.google.es/photo.png", customer["username"], "fakemailfortesting@gmail.com", "es",
             status.HTTP_400_BAD_REQUEST],

            # Negative test 11, edit customer with phone as integer
            [token, "Juan Carlos", "Utrilla Martín", 1, "http://www.google.es/photo.png", customer["username"], "fakemailfortesting@gmail.com", "es",
            status.HTTP_400_BAD_REQUEST],

            # Negative test 12, edit customer with phone as characters
            [token, "Juan Carlos", "Utrilla Martín", "e3sdsdsda", "http://www.google.es/photo.png", customer["username"], "fakemailfortesting@gmail.com", "es",
            status.HTTP_400_BAD_REQUEST],

            # Negative test 13, edit customer with invalid photo
            [token, "Juan Carlos", "Utrilla Martín", "123123123", "http:/ /www.google.es/photo.png", customer["username"], "fakemailfortesting@gmail.com", "es",
             status.HTTP_400_BAD_REQUEST],

            # Negative test 14, edit customer with token set None
            [None, "Juan Carlos", "Utrilla Martín", "666778899", "http://www.google.es/photo.png", customer["username"], "fakemailfortesting@gmail.com", "en",
             status.HTTP_401_UNAUTHORIZED],

            # Negative test 15, edit customer with token as integer
            [1, "Juan Carlos", "Utrilla Martín", "666778899", "http://www.google.es/photo.png", customer["username"], "fakemailfortesting@gmail.com", "en",
             status.HTTP_401_UNAUTHORIZED],

            # Negative test 16, edit customer with invalid token
            ["dasdaadas", "Juan Carlos", "Utrilla Martín", "666778899", "http://www.google.es/photo.png", customer["username"], "fakemailfortesting@gmail.com", "en",
             status.HTTP_401_UNAUTHORIZED],

            # Negative test 17, edit customer with first_name as None
            [token, None, "Utrilla Martín", "666778899", "http://www.google.es/photo.png", customer["username"], "fakemailfortesting@gmail.com", "en",
             status.HTTP_400_BAD_REQUEST],

            # Negative test 18, edit customer with first_name with special characters
            [token, "sdasd2123daadsad", "Utrilla Martín", "666778899", "http://www.google.es/photo.png", customer["username"], "fakemailfortesting@gmail.com", "en",
             status.HTTP_400_BAD_REQUEST],  # Cambiar id

            # Negative test 19, edit customer with first_name as integer
            [token, 1, "Utrilla Martín", "666778899", "http://www.google.es/photo.png", customer["username"], "fakemailfortesting@gmail.com", "en",
             status.HTTP_400_BAD_REQUEST],

            # Negative test 20, edit customer with last_name as None
            [token, "Juan Carlos", None, "666778899", "http://www.google.es/photo.png", customer["username"], "fakemailfortesting@gmail.com", "en",
             status.HTTP_400_BAD_REQUEST],

            # Negative test 21, edit customer with last_name with special characters
            [token, "Juan Carlos", "hfdsfsdfs23123sdas", "666778899", "http://www.google.es/photo.png", customer["username"], "fakemailfortesting@gmail.com", "en",
             status.HTTP_400_BAD_REQUEST],

            # Negative test 22, edit customer with last_name as integer
            [token, "Juan Carlos", 1, "666778899", "http://www.google.es/photo.png", customer["username"], "fakemailfortesting@gmail.com", "en",
             status.HTTP_400_BAD_REQUEST],

            # Negative test 23, edit customer with phone as integer
            [token, "Juan Carlos", "Utrilla Martín", 1, "http://www.google.es/photo.png", customer["username"], "fakemailfortesting@gmail.com", "en",
            status.HTTP_400_BAD_REQUEST],

            # Negative test 24, edit customer with phone as characters
            [token, "Juan Carlos", "Utrilla Martín", "e3sdsdsda", "http://www.google.es/photo.png", customer["username"], "fakemailfortesting@gmail.com", "en",
             status.HTTP_400_BAD_REQUEST],

            # Negative test 25, edit customer with invalid photo
            [token, "Juan Carlos", "Utrilla Martín", "123123123", "http:/ /www.google.es/photo.png", customer["username"], "fakemailfortesting@gmail.com", "en",
             status.HTTP_400_BAD_REQUEST],

            # Negative test 26, edit customer with username set as None
            [token, "Juan Carlos", "Utrilla Martín", "123123123", "http:/ /www.google.es/photo.png",
             None, "fakemailfortesting@gmail.com", "en",
             status.HTTP_400_BAD_REQUEST],

            # Negative test 27, edit customer with username set as integer
            [token, "Juan Carlos", "Utrilla Martín", "123123123", "http:/ /www.google.es/photo.png",
             1, "fakemailfortesting@gmail.com", "en",
             status.HTTP_400_BAD_REQUEST],

            # Negative test 28, edit customer with email set as None
            [token, "Juan Carlos", "Utrilla Martín", "123123123", "http:/ /www.google.es/photo.png",
             customer["username"], None, "en",
             status.HTTP_400_BAD_REQUEST],

            # Negative test 29, edit customer with email set as integer
            [token, "Juan Carlos", "Utrilla Martín", "123123123", "http:/ /www.google.es/photo.png",
             customer["username"], 1, "en",
             status.HTTP_400_BAD_REQUEST],
        ]

        print("-------- Edit personal information testing --------")

        indice = 1

        for data in payload:
            print("---> Test " + str(indice))
            self.template_edit_customer_information(data)
            indice += 1

    def template_edit_customer_information(self, args):
        status_expected = args[-1]
        language = args[-2]

        data = self.generate_data(args)

        response = self.client.put("/customer/" + str(self.sharedData['customer_id']) + "/", data, format="json",
                                   HTTP_AUTHORIZATION='Token ' + str(args[0]),
                                   HTTP_ACCEPT_LANGUAGE=language)
        self.assertEqual(status_expected, response.status_code)

        print("\nOk - Status expected: " + str(status_expected) + "\n")

