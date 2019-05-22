from rest_framework.test import APITransactionTestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from Grooving.models import Performance, ArtisticGender, Customer, Artist, Portfolio, User, Calendar, PaymentPackage, \
    EventLocation, Zone
from datetime import datetime
from django.contrib.auth.hashers import make_password


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
            "artisticName": args[7]
        }

    def test_driver_register_artist(self):
        print("------------- Starting test -------------")

        payload = [

            # Positive test 1, create an artist with language spanish
            ["David", "Romero Esparraga", "artist1", "elArtistaEspañol", "elArtistaEspañol", "utri2099@gmail.com",
             "http://www.google.com/image.png", "El pescailla", "es", status.HTTP_201_CREATED],

            # Positive test 2, create an artist with english language
            ["Miguel", "Barahona Estevez", "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "en", status.HTTP_201_CREATED],

            # Negative test 3, create an artist with existing artisticName
            ["Miguel", "Barahona Estevez", "sdadwa", "elArtistaIngles", "elArtistaIngles", "utri210das0@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 4, create an artist with existing username
            ["Miguel", "Barahona Estevez", "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 5, create an artist with first_name set to None
            [None, "Barahona Estevez", "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 6, create an artist with empty first_name
            ["", "Barahona Estevez", "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 7, create an artist with first_name with number & special characters
            ["Poli111$car", "Barahona Estevez", "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 8, create an artist with last_name set to None
            ["Policarco", None, "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 9, create an artist with empty last_name
            ["Policarco", "", "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 10, create an artist with last_name with special characters
            ["Policarco", "Mi123$", "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 11, create an artist with username set to None
            ["Policarco", "Mi123$", None, "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 12, create an artist with empty username
            ["Policarco", "Hernandez", "", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 13, create an artist with existing username
            ["Policarco", "Hernandez", "artist1", "elArtistaIngles", "elArtistaIngles", "utri28100@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 14, create an artist with password None
            ["Policarco", "Mi123$", "artist2", None, "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 15, create an artist with empty password
            ["Policarco", "Miguelin", "artist2", "", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 16, create an artist with passwords that size lower than 7
            ["Policarco", "Miguelin", "artist2", "123456", "123456", "utri210dada0@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 17, create an artist with confirm_password set to None
            ["Policarco", "Miguelin", "artist2", "1234g6gt", None, "utri210dada0@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 18, create an artist with passwords that size lower than 7
            ["Policarco", "Miguelin", "artist2", "1234g6gt", "", "utri210dada0@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 19, create an artist with passwords that not match
            ["Policarco", "Miguelin", "artist2", "1234g6gt", "fsdgsdfgsdfgs", "utri210dada0@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 20, create an artist with insecure password
            ["Policarco", "Miguelin", "artist2", "1234g6gt", "1234g6gt", "",
             "http://www.google.com/image.png", "El malaguita", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 21, create an artist with insecure password
            ["Policarco", "Miguelin", "artist2", "1234g6gt", "1234g6gt", "utri210dada0@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 22, create an artist with not valid email
            ["Policarco", "Miguelin", "artist22", "12a4g6g1b3t", "12a4g6g1b3t", "holdasda",
             "http://www.google.com/image.png", "El malaguita", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 23, create an artist with not valid image
            ["Policarco", "Miguelin", "artist22", "12a4g6g1b3t", "12a4g6g1b3t", "utri210dada0@gmail.com",
             "http:/ /www.google.com/image.png", "Camela", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 24, create an artist with empty image
            ["Policarco", "Miguelin", "artist22", "12a4g6g1b3t", "12a4g6g1b3t", "utri210dada0@gmail.com",
             "h", "Camela", "en", status.HTTP_400_BAD_REQUEST],

            # Negative test 25, create an artist with language set to None
            ["Policarco", "Miguelin", "artist22", "12a4g6g1b3t", "12a4g6g1b3t", "utri210dada0@gmail.com",
             "http://www.google.com/image.png", "Camela", None, status.HTTP_400_BAD_REQUEST],

            # Negative test 26, create an artist with language not supported
            ["Policarco", "Miguelin", "artist22", "12a4g6g1b3t", "12a4g6g1b3t", "utri210dada0@gmail.com",
             "http:/ /www.google.com/image.png", "Camela", "pt", status.HTTP_400_BAD_REQUEST],

            # Negative test 27, create an artist with existing artisticName
            ["Miguel", "Barahona Estevez", "sdadwa", "elArtistaIngles", "elArtistaIngles", "utri210das0@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 28, create an artist with existing username
            ["Miguel", "Barahona Estevez", "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 29, create an artist with first_name set to None
            [None, "Barahona Estevez", "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 30, create an artist with empty first_name
            ["", "Barahona Estevez", "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 31, create an artist with first_name with number & special characters
            ["Poli111$car", "Barahona Estevez", "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 32, create an artist with last_name set to None
            ["Policarco", None, "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 33, create an artist with empty last_name
            ["Policarco", "", "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 34, create an artist with last_name with special characters
            ["Policarco", "Mi123$", "artist2", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 35, create an artist with username set to None
            ["Policarco", "Mi123$", None, "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 36, create an artist with empty username
            ["Policarco", "Hernandez", "", "elArtistaIngles", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 37, create an artist with existing username
            ["Policarco", "Hernandez", "artist1", "elArtistaIngles", "elArtistaIngles", "utri28100@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 38, create an artist with password None
            ["Policarco", "Mi123$", "artist2", None, "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 39, create an artist with empty password
            ["Policarco", "Miguelin", "artist2", "", "elArtistaIngles", "utri2100@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 40, create an artist with passwords that size lower than 7
            ["Policarco", "Miguelin", "artist2", "123456", "123456", "utri210dada0@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 41, create an artist with confirm_password set to None
            ["Policarco", "Miguelin", "artist2", "1234g6gt", None, "utri210dada0@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 42, create an artist with passwords that size lower than 7
            ["Policarco", "Miguelin", "artist2", "1234g6gt", "", "utri210dada0@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 43, create an artist with passwords that not match
            ["Policarco", "Miguelin", "artist2", "1234g6gt", "fsdgsdfgsdfgs", "utri210dada0@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 44, create an artist with insecure password
            ["Policarco", "Miguelin", "artist2", "1234g6gt", "1234g6gt", "",
             "http://www.google.com/image.png", "El malaguita", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 45, create an artist with insecure password
            ["Policarco", "Miguelin", "artist2", "1234g6gt", "1234g6gt", "utri210dada0@gmail.com",
             "http://www.google.com/image.png", "El malaguita", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 46, create an artist with not valid email
            ["Policarco", "Miguelin", "artist22", "12a4g6g1b3t", "12a4g6g1b3t", "holdasda",
             "http://www.google.com/image.png", "El malaguita", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 47, create an artist with not valid image
            ["Policarco", "Miguelin", "artist22", "12a4g6g1b3t", "12a4g6g1b3t", "utri210dada0@gmail.com",
             "http:/ /www.google.com/image.png", "Camela", "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 48 create an artist with empty image
            ["Policarco", "Miguelin", "artist22", "12a4g6g1b3t", "12a4g6g1b3t", "utri210dada0@gmail.com",
             "h", "Camela", "es", status.HTTP_400_BAD_REQUEST]

        ]
        print("-------- Creating artist testing --------")
        for data in payload:
            print("---> Test " + str(payload.index(data) + 1))
            self.template_register_user(data)

    def template_register_user(self, args):
        status_expected = args[-1]
        language = args[-2]

        data = self.generateData(args)

        response = self.client.post("/signupArtist/", data, format="json", HTTP_ACCEPT_LANGUAGE=language)
        self.assertEqual(status_expected, response.status_code)

        print("\nOk - Status expected: " + str(status_expected) + "\n")


class EditArtistPersonalInformation(APITransactionTestCase):
    sharedData = {

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

        portfolio = Portfolio.objects.create(artisticName='Tamta',
                                             artist=artist,
                                             banner='http://www.ddi.com.au/wp-content/uploads/AdobeStock_115567415.jpeg',
                                             biography='Tamta, is a Georgian-Greek singer. She first achieved popularity in Greece and Cyprus in 2004 for her participation in Super Idol Greece, in which she placed second. She went on to release several charting albums and singles in Greece and Cyprus. Goduadze became a mentor on X Factor Georgia in 2014, and The X Factor Greece in 2016.')
        portfolio.save()

        self.sharedData['artist_id'] = artist.id
        self.sharedData['user_artist_id'] = user_artist.id

    def generate_data(self, args):
        return {
            "first_name": args[1],
            "last_name": args[2],
            "phone": args[3],
            "photo": args[4],
            "paypalAccount": args[5],
            "artisticName": args[6],
            "username": args[7],
            "email": args[8]
        }

    def test_driver_edit_customer_personal_information(self):
        print("------------- Starting test -------------")

        artist = {"username": "artist1", "password": "artista1"}
        response = self.client.post("/api/login/", artist, format='json')

        token_num = response.get("x-auth")

        # Con esto evitamos problemas si el token no existe en bd

        token = ''

        try:
            token = Token.objects.all().filter(pk=token_num).first().key
        except:
            pass

        payload = [
            # Positive test 1, edit artist personal information
            [token, "Juan Carlos", "Utrilla Martín", "666778899", "http://www.google.es/photo.png", "paypal@gmail.com", "Los sobaos", artist["username"], "fakemailfortesting@gmail.com",
             "es", status.HTTP_200_OK],

            # Negative test 2, edit artist with token set None
            [None, "Juan Carlos", "Utrilla Martín", "666778899", "http://www.google.es/photo.png", "paypal2@gmail.com", "Los sobaos 2", artist["username"], "fakemailfortesting@gmail.com",
             "es", status.HTTP_401_UNAUTHORIZED],

            # Negative test 3, edit artist with token as integer
            [1, "Juan Carlos", "Utrilla Martín", "666778899", "http://www.google.es/photo.png", "paypal2@gmail.com", "Los sobaos 2", artist["username"], "fakemailfortesting@gmail.com",
             "es",
             status.HTTP_401_UNAUTHORIZED],

            # Negative test 4, edit artist with invalid token
            ["dasdaadas", "Juan Carlos", "Utrilla Martín", "666778899", "http://www.google.es/photo.png", "paypal2@gmail.com", "Los sobaos 2", artist["username"], "fakemailfortesting@gmail.com",
             "es", status.HTTP_401_UNAUTHORIZED],

            # Negative test 5, edit artist with first_name as None
            [token, None, "Utrilla Martín", "666778899", "http://www.google.es/photo.png", "paypal2@gmail.com", "Los sobaos 2", artist["username"], "fakemailfortesting@gmail.com",
             "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 6, edit artist with first_name with special characters
            [token, "sdasd2123daadsad", "Utrilla Martín", "666778899", "http://www.google.es/photo.png", "paypal2@gmail.com", "Los sobaos 2", artist["username"], "fakemailfortesting@gmail.com",
             "es", status.HTTP_400_BAD_REQUEST],

            # Negative test 7, edit artist with first_name as integer
            [token, 1, "Utrilla Martín", "666778899", "http://www.google.es/photo.png", "paypal2@gmail.com", "Los sobaos 2", artist["username"], "fakemailfortesting@gmail.com", "es",
             status.HTTP_400_BAD_REQUEST],

            # Negative test 8, edit artist with last_name as None
            [token, "Juan Carlos", None, "666778899", "http://www.google.es/photo.png", "paypal2@gmail.com", "Los sobaos 2", artist["username"], "fakemailfortesting@gmail.com", "es",
             status.HTTP_400_BAD_REQUEST],

            # Negative test 9, edit artist with last_name with special characters
            [token, "Juan Carlos", "hfdsfsdfs23123sdas", "666778899", "http://www.google.es/photo.png", "paypal2@gmail.com", "Los sobaos 2", artist["username"], "fakemailfortesting@gmail.com", "es",
             status.HTTP_400_BAD_REQUEST],

            # Negative test 10, edit artist with last_name as integer
            [token, "Juan Carlos", 1, "666778899", "http://www.google.es/photo.png", "paypal2@gmail.com", "Los sobaos 2", artist["username"], "fakemailfortesting@gmail.com", "es",
             status.HTTP_400_BAD_REQUEST],

            # Negative test 11, edit artist with phone as integer
            [token, "Juan Carlos", "Utrilla Martín", 1, "http://www.google.es/photo.png", "paypal2@gmail.com", "Los sobaos 2", artist["username"], "fakemailfortesting@gmail.com", "es",
            status.HTTP_400_BAD_REQUEST],

            # Negative test 12, edit artist with phone as characters
            [token, "Juan Carlos", "Utrilla Martín", "e3sdsdsda", "http://www.google.es/photo.png", "paypal2@gmail.com", "Los sobaos 2", artist["username"], "fakemailfortesting@gmail.com", "es",
            status.HTTP_400_BAD_REQUEST],

            # Negative test 13, edit artist with invalid photo
            [token, "Juan Carlos", "Utrilla Martín", "123123123", "http:/ /www.google.es/photo.png", "paypal2@gmail.com", "Los sobaos 2", artist["username"], "fakemailfortesting@gmail.com", "es",
             status.HTTP_400_BAD_REQUEST],

            # Negative test 14, edit artist with token set None
            [None, "Juan Carlos", "Utrilla Martín", "666778899", "http://www.google.es/photo.png", "paypal2@gmail.com", "Los sobaos 2", artist["username"], "fakemailfortesting@gmail.com", "en",
             status.HTTP_401_UNAUTHORIZED],

            # Negative test 15, edit artist with token as integer
            [1, "Juan Carlos", "Utrilla Martín", "666778899", "http://www.google.es/photo.png", "paypal2@gmail.com", "Los sobaos 2", artist["username"], "fakemailfortesting@gmail.com", "en",
             status.HTTP_401_UNAUTHORIZED],

            # Negative test 16, edit artist with invalid token
            ["dasdaadas", "Juan Carlos", "Utrilla Martín", "666778899", "http://www.google.es/photo.png", "paypal2@gmail.com", "Los sobaos 2", artist["username"], "fakemailfortesting@gmail.com", "en",
             status.HTTP_401_UNAUTHORIZED],

            # Negative test 17, edit artist with first_name as None
            [token, None, "Utrilla Martín", "666778899", "http://www.google.es/photo.png", "paypal2@gmail.com", "Los sobaos 2", artist["username"], "fakemailfortesting@gmail.com", "en",
             status.HTTP_400_BAD_REQUEST],

            # Negative test 18, edit artist with first_name with special characters
            [token, "sdasd2123daadsad", "Utrilla Martín", "666778899", "http://www.google.es/photo.png", "paypal2@gmail.com", "Los sobaos 2", artist["username"], "fakemailfortesting@gmail.com", "en",
             status.HTTP_400_BAD_REQUEST],  # Cambiar id

            # Negative test 19, edit artist with first_name as integer
            [token, 1, "Utrilla Martín", "666778899", "http://www.google.es/photo.png", "paypal2@gmail.com", "Los sobaos 2", artist["username"], "fakemailfortesting@gmail.com", "en",
             status.HTTP_400_BAD_REQUEST],

            # Negative test 20, edit artist with last_name as None
            [token, "Juan Carlos", None, "666778899", "http://www.google.es/photo.png", "paypal2@gmail.com", "Los sobaos 2", artist["username"], "fakemailfortesting@gmail.com", "en",
             status.HTTP_400_BAD_REQUEST],

            # Negative test 21, edit artist with last_name with special characters
            [token, "Juan Carlos", "hfdsfsdfs23123sdas", "666778899", "http://www.google.es/photo.png", "paypal2@gmail.com", "Los sobaos 2", artist["username"], "fakemailfortesting@gmail.com", "en",
             status.HTTP_400_BAD_REQUEST],

            # Negative test 22, edit artist with last_name as integer
            [token, "Juan Carlos", 1, "666778899", "http://www.google.es/photo.png", "paypal2@gmail.com", "Los sobaos 2", artist["username"], "fakemailfortesting@gmail.com", "en",
             status.HTTP_400_BAD_REQUEST],

            # Negative test 23, edit artist with phone as integer
            [token, "Juan Carlos", "Utrilla Martín", 1, "http://www.google.es/photo.png", "paypal2@gmail.com", "Los sobaos 2", artist["username"], "fakemailfortesting@gmail.com", "en",
            status.HTTP_400_BAD_REQUEST],

            # Negative test 24, edit artist with phone as characters
            [token, "Juan Carlos", "Utrilla Martín", "e3sdsdsda", "http://www.google.es/photo.png", "paypal2@gmail.com", "Los sobaos 2", artist["username"], "fakemailfortesting@gmail.com", "en",
             status.HTTP_400_BAD_REQUEST],

            # Negative test 25, edit artist with invalid photo
            [token, "Juan Carlos", "Utrilla Martín", "123123123", "http:/ /www.google.es/photo.png", "paypal2@gmail.com", "Los sobaos 2", artist["username"], "fakemailfortesting@gmail.com", "en",
             status.HTTP_400_BAD_REQUEST],

            # Negative test 26, edit artist with username as None
            [token, "Juan Carlos", "Utrilla Martín", "123123123", "http:/ /www.google.es/photo.png",
             "paypal2@gmail.com", "Los sobaos 2", None, "fakemailfortesting@gmail.com", "en",
             status.HTTP_400_BAD_REQUEST],

            # Negative test 27, edit artist with username as integer
            [token, "Juan Carlos", "Utrilla Martín", "123123123", "http:/ /www.google.es/photo.png",
             "paypal2@gmail.com", "Los sobaos 2", 1, "fakemailfortesting@gmail.com", "en",
             status.HTTP_400_BAD_REQUEST],

            # Negative test 28, edit artist with email as None
            [token, "Juan Carlos", "Utrilla Martín", "123123123", "http:/ /www.google.es/photo.png",
             "paypal2@gmail.com", "Los sobaos 2", artist["username"], None, "en",
             status.HTTP_400_BAD_REQUEST],

            # Negative test 29, edit artist with email as integer
            [token, "Juan Carlos", "Utrilla Martín", "123123123", "http:/ /www.google.es/photo.png",
             "paypal2@gmail.com", "Los sobaos 2", artist["username"], 1, "en",
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

        response = self.client.put("/artist/" + str(self.sharedData['artist_id']) + "/", data, format="json",
                                   HTTP_AUTHORIZATION='Token ' + str(args[0]),
                                   HTTP_ACCEPT_LANGUAGE=language)
        self.assertEqual(status_expected, response.status_code)

        print("\nOk - Status expected: " + str(status_expected) + "\n")


class ListArtistByGenre(APITransactionTestCase):

    def setUp(self):
        user2_artist1 = User.objects.create(username='artist1', password=make_password('artist1'),
                                            first_name='Manolo', last_name='Manolez',
                                            email='artist1@isamail.com')
        user2_artist1.save()

        artist1 = Artist.objects.create(user=user2_artist1)
        artist1.save()
        self.artistId = artist1.pk
        gender = ArtisticGender.objects.create(name_es="Roca", name_en="Rock")
        gender.save()
        portfolio1 = Portfolio.objects.create(artisticName="Manolo el Guitarras", artist=artist1)
        portfolio1.artisticGender.add(gender)
        portfolio1.save()

        user2_artist2 = User.objects.create(username='artist2', password=make_password('artist2'),
                                            first_name='Manolin', last_name='Manolinez',
                                            email='artist2@isamail.com')
        user2_artist2.save()

        artist2 = Artist.objects.create(user=user2_artist2)
        artist2.save()
        self.artistId = artist1.pk
        gender2 = ArtisticGender.objects.create(name_es="Popular", name_en="Pop")
        gender2.save()
        portfolio2 = Portfolio.objects.create(artisticName="Manolin el Guitarras", artist=artist2)
        portfolio2.artisticGender.add(gender2)
        portfolio2.save()

    def test_driver_list_artist(self):
        payload = [
            [None, 2, 200],
            ["Rock", 1, 200],
            ["rock", 1, 200],
            ["Roca", 1, 200],
            ["Pop", 1, 200],

        ]

        indice = 1
        for data in payload:
            print("---> Test " + str(indice) + " es")
            self.template_list_artist(data, "es")
            print("---> Test " + str(indice) + " en")
            self.template_list_artist(data, "en")
            indice += 1

    def template_list_artist(self, arg, lang):
        http_code = arg[-1]
        genre = arg[0]
        length = arg[1]
        if genre is None:
            genre = ""
        response = self.client.get("/artists/?artisticGender="+genre, HTTP_ACCEPT_LANGUAGE=lang)
        print(response.status_code)
        self.assertEqual(http_code, response.status_code)
        print(response.data)
        self.assertEqual(length, len(response.data))






'''
class ShowArtistInformation(TestCase):
    
    def test_show_personal_information_artist(self):

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

        response2 = self.client.get('/artist/personalInformation/', format='json', HTTP_AUTHORIZATION='Token ' + token.key)
        self.assertEqual(response2.status_code, 200)
        result = response2.json()
        item_dict = response2.json()
        self.assertTrue(len(item_dict) == 7)

        self.client.logout()

    def test_show_personal_information_customer_forbidden(self):

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

        response2 = self.client.get('/artist/personalInformation/', format='json',
                                    HTTP_AUTHORIZATION='Token ' + token.key)
        self.assertEqual(response2.status_code, 403)
        self.client.logout()

    def test_show_personal_information_admin_forbidden(self):

        user1_artist1 = User.objects.create(username='artist1', password=make_password('artist1'),
                                            first_name='Bunny', last_name='Fufuu',
                                            email='artist1@gmail.com', is_staff=True)
        user1_artist1.save()

        self.client.force_login(user1_artist1)

        response2 = self.client.get('/artist/personalInformation/', format='json')
        self.assertEqual(response2.status_code, 403)
        self.client.logout()

    def test_show_personal_information_anonymous_forbidden(self):

        response = self.client.get('/artist/personalInformation/', format='json')
        self.assertEqual(response.status_code, 403)


class ListArtistTestCase(TestCase):

    def test_list_artists(self):

        user1_artist1 = User.objects.create(username='artist1', password=make_password('artist1'),
                                            first_name='Bunny', last_name='Fufuu',
                                            email='artist1@gmail.com')
        user1_artist1.save()

        zone1 = Zone.objects.create(name="Sevilla Sur")
        zone1.save()

        portfolio1 = Portfolio.objects.create(artisticName="BunnyFuFuu")
        portfolio1.zone.add(zone1)
        portfolio1.save()

        performance1 = Performance.objects.create(info='Information', hours='2.5', price=300)

        paymentPackage = PaymentPackage.objects.create(description='description of a payment', currency='EUR',
                                                       portfolio=portfolio1, performance=performance1)

        artist1 = Artist.objects.create(user=user1_artist1, portfolio=portfolio1, phone='600304999')
        artist1.save()

        response = self.client.get('/artists/', format='json')
        self.assertEqual(response.status_code, 200)
        item_dict = response.json()
        self.assertTrue(len(item_dict['results']) != 0)

    def test_list_artists_filter_artistic_name(self):

        user = User()
        user.email = "juan@juan.com"
        user.username = "artist"
        user.password = "artist"
        user.id = "43"
        user.save()

        portfolio1 = Portfolio()
        portfolio1.id = "2"
        portfolio1.artisticName = "Jose"
        portfolio1.save()

        paymentPackage = PaymentPackage()
        paymentPackage.id = "87"
        paymentPackage.description = "paymentPackage description"
        paymentPackage.appliedVAT = "0.07"
        paymentPackage.portfolio = portfolio1
        paymentPackage.save()

        artista = Artist()
        artista.photo = "https://conectandomeconlau.com.co/wp-content/uploads/2018/03/%C2%BFTienes-las-caracteri%CC%81sticas-para-ser-un-Artista.png"
        artista.id = "56"
        artista.iban = "AD1400080001001234567890"
        artista.phone = "999999999"
        artista.paypalAccount = "user=artist,password=artist"
        artista.user_id = "43"
        artista.portfolio = portfolio1
        artista.save()

        user2 = User()
        user2.email = "juanjo@juanjo.com"
        user2.username = "artist2"
        user2.password = "artist2"
        user2.id = "44"
        user2.save()

        portfolio2 = Portfolio()
        portfolio2.id = "3"
        portfolio2.artisticName = "María se fue a la cama a las diez"
        portfolio2.save()

        paymentPackage2 = PaymentPackage()
        paymentPackage2.id = "88"
        paymentPackage2.description = "paymentPackage description 2222222222"
        paymentPackage2.appliedVAT = "0.07"
        paymentPackage2.portfolio = portfolio2
        paymentPackage2.save()

        artista2 = Artist()
        artista2.photo = "https://conectandomeconlau.com.co/wp-content/uploads/2018/03/%C2%BFTienes-las-caracteri%CC%81sticas-para-ser-un-Artista.png"
        artista2.id = "57"
        artista2.iban = "AD1400080001001234567890"
        artista2.phone = "999999999"
        artista2.paypalAccount = "user=artist,password=artist"
        artista2.user_id = "44"
        artista2.portfolio = portfolio2
        artista2.save()

        response = self.client.get('/artists/?artisticName=Jose', format='json')
        item_dict = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(item_dict['results']) != 0)


    def test_list_artists_filter_artistic_gender(self):
        user = User()
        user.email = "juan@juan.com"
        user.username = "artist"
        user.password = "artist"
        user.id = "43"
        user.save()

        artisticGender2 = ArtisticGender()
        artisticGender2.id = "1"
        artisticGender2.name = "Pop"
        artisticGender2.parentGender = None
        artisticGender2.save()

        portfolio1 = Portfolio()
        portfolio1.id = "2"
        portfolio1.artisticName = "Jose"
        portfolio1.save()
        portfolio1.artisticGender.add(artisticGender2)
        portfolio1.save()

        paymentPackage = PaymentPackage()
        paymentPackage.id = "87"
        paymentPackage.description = "paymentPackage description"
        paymentPackage.appliedVAT = "0.07"
        paymentPackage.portfolio = portfolio1
        paymentPackage.save()

        artista = Artist()
        artista.photo = "https://conectandomeconlau.com.co/wp-content/uploads/2018/03/%C2%BFTienes-las-caracteri%CC%81sticas-para-ser-un-Artista.png"
        artista.id = "56"
        artista.iban = "AD1400080001001234567890"
        artista.phone = "999999999"
        artista.paypalAccount = "user=artist,password=artist"
        artista.user_id = "43"
        artista.portfolio = portfolio1
        artista.save()

        user2 = User()
        user2.email = "juanjo@juanjo.com"
        user2.username = "artist2"
        user2.password = "artist2"
        user2.id = "44"
        user2.save()

        artisticGender = ArtisticGender()
        artisticGender.id = "2"
        artisticGender.name = "Rock"
        artisticGender.parentGender = None
        artisticGender.save()

        portfolio2 = Portfolio()
        portfolio2.id = "3"
        portfolio2.artisticName = "María se fue a la cama a las diez"
        portfolio2.save()
        portfolio2.artisticGender.add(artisticGender)
        portfolio2.save()

        paymentPackage2 = PaymentPackage()
        paymentPackage2.id = "88"
        paymentPackage2.description = "paymentPackage description 2222222222"
        paymentPackage2.appliedVAT = "0.07"
        paymentPackage2.portfolio = portfolio2
        paymentPackage2.save()

        artista2 = Artist()
        artista2.photo = "https://conectandomeconlau.com.co/wp-content/uploads/2018/03/%C2%BFTienes-las-caracteri%CC%81sticas-para-ser-un-Artista.png"
        artista2.id = "57"
        artista2.iban = "AD1400080001001234567890"
        artista2.phone = "999999999"
        artista2.paypalAccount = "user=artist,password=artist"
        artista2.user_id = "44"
        artista2.portfolio = portfolio2
        artista2.save()

        response = self.client.get('/artists/?artisticGender=Rock', format='json')
        item_dict = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(item_dict['results']) != 0)


    def test_list_artists_filter_artistic_gender_no_matches(self):
        user = User()
        user.email = "juan@juan.com"
        user.username = "artist"
        user.password = "artist"
        user.id = "43"
        user.save()

        artisticGender2 = ArtisticGender()
        artisticGender2.id = "1"
        artisticGender2.name = "Pop"
        artisticGender2.parentGender = None
        artisticGender2.save()

        portfolio1 = Portfolio()
        portfolio1.id = "2"
        portfolio1.artisticName = "Jose"
        portfolio1.save()

        portfolio1.artisticGender.add(artisticGender2)
        portfolio1.save()

        paymentPackage = PaymentPackage()
        paymentPackage.id = "87"
        paymentPackage.description = "paymentPackage description"
        paymentPackage.appliedVAT = "0.07"
        paymentPackage.portfolio = portfolio1
        paymentPackage.save()

        artista = Artist()
        artista.photo = "https://conectandomeconlau.com.co/wp-content/uploads/2018/03/%C2%BFTienes-las-caracteri%CC%81sticas-para-ser-un-Artista.png"
        artista.id = "56"
        artista.iban = "AD1400080001001234567890"
        artista.phone = "999999999"
        artista.paypalAccount = "user=artist,password=artist"
        artista.user_id = "43"
        artista.portfolio = portfolio1
        artista.save()

        user2 = User()
        user2.email = "juanjo@juanjo.com"
        user2.username = "artist2"
        user2.password = "artist2"
        user2.id = "44"
        user2.save()

        artisticGender = ArtisticGender()
        artisticGender.id = "2"
        artisticGender.name = "Rock"
        artisticGender.parentGender = None
        artisticGender.save()

        portfolio2 = Portfolio()
        portfolio2.id = "3"
        portfolio2.artisticName = "María se fue a la cama a las diez"
        portfolio2.save()
        portfolio2.artisticGender.add(artisticGender)
        portfolio2.save()

        paymentPackage2 = PaymentPackage()
        paymentPackage2.id = "88"
        paymentPackage2.description = "paymentPackage description 2222222222"
        paymentPackage2.appliedVAT = "0.07"
        paymentPackage2.portfolio = portfolio2
        paymentPackage2.save()

        artista2 = Artist()
        artista2.photo = "https://conectandomeconlau.com.co/wp-content/uploads/2018/03/%C2%BFTienes-las-caracteri%CC%81sticas-para-ser-un-Artista.png"
        artista2.id = "57"
        artista2.iban = "AD1400080001001234567890"
        artista2.phone = "999999999"
        artista2.paypalAccount = "user=artist,password=artist"
        artista2.user_id = "44"
        artista2.portfolio = portfolio2
        artista2.save()

        response = self.client.get('/artists/?artisticGender=Country', format='json')
        item_dict = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(item_dict['results']) == 0)


    def test_list_artists_filter_artistic_gender_parent_match(self):
        user = User()
        user.email = "juan@juan.com"
        user.username = "artist"
        user.password = "artist"
        user.id = "43"
        user.save()

        artisticGender2 = ArtisticGender()
        artisticGender2.id = "1"
        artisticGender2.name = "Musica"
        artisticGender2.parentGender = None
        artisticGender2.save()

        portfolio1 = Portfolio()
        portfolio1.id = "2"
        portfolio1.artisticName = "Jose"
        portfolio1.save()
        portfolio1.artisticGender.add(artisticGender2)
        portfolio1.save()

        paymentPackage = PaymentPackage()
        paymentPackage.id = "87"
        paymentPackage.description = "paymentPackage description"
        paymentPackage.appliedVAT = "0.07"
        paymentPackage.portfolio = portfolio1
        paymentPackage.save()

        artista = Artist()
        artista.photo = "https://conectandomeconlau.com.co/wp-content/uploads/2018/03/%C2%BFTienes-las-caracteri%CC%81sticas-para-ser-un-Artista.png"
        artista.id = "56"
        artista.iban = "AD1400080001001234567890"
        artista.phone = "999999999"
        artista.paypalAccount = "user=artist,password=artist"
        artista.user_id = "43"
        artista.portfolio = portfolio1
        artista.save()

        user2 = User()
        user2.email = "juanjo@juanjo.com"
        user2.username = "artist2"
        user2.password = "artist2"
        user2.id = "44"
        user2.save()

        artisticGender = ArtisticGender()
        artisticGender.id = "2"
        artisticGender.name = "Rock"
        artisticGender.parentGender = artisticGender2
        artisticGender.save()

        artisticGender3 = ArtisticGender()
        artisticGender3.id = "3"
        artisticGender3.name = "Punk"
        artisticGender3.parentGender = artisticGender
        artisticGender3.save()

        portfolio2 = Portfolio()
        portfolio2.id = "3"
        portfolio2.artisticName = "María se fue a la cama a las diez"
        portfolio2.save()
        portfolio2.artisticGender.add(artisticGender3)
        portfolio2.save()

        paymentPackage2 = PaymentPackage()
        paymentPackage2.id = "88"
        paymentPackage2.description = "paymentPackage description 2222222222"
        paymentPackage2.appliedVAT = "0.07"
        paymentPackage2.portfolio = portfolio2
        paymentPackage2.save()

        artista2 = Artist()
        artista2.photo = "https://conectandomeconlau.com.co/wp-content/uploads/2018/03/%C2%BFTienes-las-caracteri%CC%81sticas-para-ser-un-Artista.png"
        artista2.id = "57"
        artista2.iban = "AD1400080001001234567890"
        artista2.phone = "999999999"
        artista2.paypalAccount = "user=artist,password=artist"
        artista2.user_id = "44"
        artista2.portfolio = portfolio2
        artista2.save()

        response = self.client.get('/artists/?artisticGender=Musica', format='json')
        item_dict = response.json()
        self.assertEqual(response.status_code, 200)

        self.assertTrue(len(item_dict['results']) != 0)
    '''
