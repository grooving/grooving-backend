from Grooving.models import  Artist, Portfolio, User, Customer, Calendar, Zone, SystemConfiguration
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.test import APITransactionTestCase


class CalendarTestCase(APITransactionTestCase):

    def setUp(self):
        your_email = 'pruebatestinggrooving@gmail.com'
        print('-------- Setup test --------')

        print('---- Creating calendar test ----')

        print('---- Creating user ----')

        user1_artist10 = User.objects.create(username='artist1', password=make_password('artist1artist1'),
                                             first_name='Carlos', last_name='Campos Cuesta',
                                             email=your_email)
        Token.objects.create(user=user1_artist10)

        user1_artist10.save()

        print('---- Creating artist ----')

        artist1 = Artist.objects.create(user=user1_artist10, rating=5.0, phone='600304999',
                                        language='en',
                                        photo='https://img.discogs.com/jgyNBtPsY4DiLegwMrOC9N_yOc4=/600x600/smart/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/A-1452461-1423476836-6354.jpeg.jpg',
                                        iban='ES6621000418401234567891', paypalAccount='tamta.info@gmail.com')

        artist1.save()

        user2_customer1 = User.objects.create(username='customer1', password=make_password('customer1customer1'),
                                              first_name='Rafael', last_name='Esquivias Ramírez',
                                              email=your_email)

        user2_customer1.save()

        Token.objects.create(user=user2_customer1)

        user1_artist2 = User.objects.create(username='artist2', password=make_password('artist2artist2'),
                                             first_name='Pablo', last_name='Motos',
                                             email=your_email)
        Token.objects.create(user=user1_artist2)

        user1_artist2.save()

        artist2 = Artist.objects.create(user=user1_artist2, rating=5.0, phone='600304999',
                                        language='en',
                                        photo='https://img.discogs.com/jgyNBtPsY4DiLegwMrOC9N_yOc4=/600x600/smart/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/A-1452461-1423476836-6354.jpeg.jpg',
                                        iban='ES6621000418401234567891', paypalAccount='tamta.info@gmail.com')

        artist2.save()

        print('---- Creating customer ----')

        customer1 = Artist.objects.create(user=user2_customer1, rating=5.0, phone='600304999',
                                        language='en',
                                        photo='https://img.discogs.com/jgyNBtPsY4DiLegwMrOC9N_yOc4=/600x600/smart/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/A-1452461-1423476836-6354.jpeg.jpg',
                                        iban='ES6621000418401234567891', paypalAccount='tamto.info@gmail.com')

        customer1.save()



        print('---- Creating zone ----')

        zone1 = Zone.objects.create(name='Andalucía')

        zone1.save()

        print('---- Creating portfolio ----')

        portfolio1 = Portfolio.objects.create(artist=artist1, artisticName="Los rebujitos")
        portfolio1.zone.add(zone1)
        portfolio1.save()

        calendar = Calendar.objects.create(days=[], portfolio=portfolio1)

        calendar.save()

        SystemConfiguration.objects.create(minimumPrice=20.0, currency='EUR', paypalTax='3.4', creditCardTax='1.9',
                                           vat='21',
                                           profit='10',
                                           corporateEmail='grupogrooving@gmail.com',
                                           reportEmail='grupogrooving@gmail.com',
                                           appName='Grooving',
                                           slogan='Connecting artist with you',
                                           logo='',
                                           privacyText_en='Privacity',
                                           privacyText_es='Privacidad',
                                           aboutUs_en='About us',
                                           aboutUs_es='Sobre nosotros',
                                           termsText_es='Términos y condiciones',
                                           termsText_en='Terms and conditions')

    # Driver function

    def test_driver_edit_calendar(self):

        print('Start test - edit calendar as the intended artist')
        data1 = {"username": "artist1", "password": "artist1artist1"}
        response = self.client.post("/api/login/", data1, format='json')

        token_num = response.get('x-auth')

        data3 = {"username": "artist2", "password": "artist2artist2"}
        response3 = self.client.post("/api/login/", data3, format='json')

        token_num3 = response3.get('x-auth')

        data2 = {"username": "customer1", "password": "customer1customer1"}
        response2 = self.client.post("/api/login/", data2, format='json')

        token_num2 = response2.get('x-auth')

        #Para evitar problemas si el token no existe en bd
        token = ''
        try:
            token = Token.objects.all().filter(pk=token_num).first().key
        except:
            pass
        token2 = ''
        try:
            token2 = Token.objects.all().filter(pk=token_num2).first().key
        except:
            pass
        token3 = ''
        try:
            token3 = Token.objects.all().filter(pk=token_num3).first().key
        except:
            pass
        # Data payload
        portfolio1 = Portfolio.objects.all().first().id

        print(token)

        payload = [

            #Test positivo 1, con dia
            [token, ['2019-09-20'], portfolio1, 200],
            #Test positivo 2, sin dias
            [token, [], portfolio1, 200],
            #Test negativo 1, fecha equivocada
            [token, ['2019/08/20'], portfolio1, 400],
            # Test negativo 2, id invalido
            [token, ['2019-08-20'], 'a', 400],
            # Test negativo 3, no se pasan días al calendar
            [token, '', 'a', 400],
            # Test negativo 4, no se pasan días al calendar (ahora es un None)
            [token, None, portfolio1, 400],
            # Test negativo 5, no se pasa un id de portfolio
            [token, [], None, 400],
            # Test negativo 6, se pasa un id 0 de portfolio
            [token, [], 0, 400],
            # Test negativo 7, customer
            [token2, ['2019-09-20'], portfolio1, 403],
            # Test negativo 8, artist incorrecto
            [token3, [], portfolio1, 403],
            #Test negativo 9, no se pasa un array
            [token, '2019-09-14', portfolio1, 400]

        ]
        contador = 0
        for data in payload:
            contador = contador + 1
            print('Test número '+str(contador))
            print(str(data))
            self.template_edit_calendar(data)

    def generateData(self, args):
        return {'days': args[1],
                'portfolio': args[2]}

    # Template function

    def template_edit_calendar(self, args):

        data = self.generateData(args)

        response_es = self.client.put('/calendar/1/', data, format='json', HTTP_AUTHORIZATION='Token ' + args[0],
                                    HTTP_ACCEPT_LANGUAGE='es')

        self.assertEqual(args[-1], response_es.status_code)

        response_en = self.client.put('/calendar/1/', data, format='json', HTTP_AUTHORIZATION='Token ' + args[0],
                                   HTTP_ACCEPT_LANGUAGE='en')

        self.assertEqual(args[-1], response_en.status_code)
