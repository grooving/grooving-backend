'''from Grooving.models import  Artist, Portfolio, User,  PaymentPackage, Customer, EventLocation, Zone, \
    Performance, SystemConfiguration
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

        print('---- Creating artist ----')

        artist1 = Artist.objects.create(user=user1_artist10, rating=5.0, phone='600304999',
                                        language='en',
                                        photo='https://img.discogs.com/jgyNBtPsY4DiLegwMrOC9N_yOc4=/600x600/smart/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/A-1452461-1423476836-6354.jpeg.jpg',
                                        iban='ES6621000418401234567891', paypalAccount='tamta.info@gmail.com')

        user2_customer1 = User.objects.create(username='customer1', password=make_password('customer1customer1'),
                                              first_name='Rafael', last_name='Esquivias Ramírez',
                                              email=your_email)
        Token.objects.create(user=user2_customer1)

        print('---- Creating customer ----')

        customer1 = Customer.objects.create(user=user2_customer1, phone='639154189', holder='Rafael Esquivias Ramírez',
                                            expirationDate='2020-10-01', number='4651001401188232',
                                            language='en',
                                            paypalAccount='rafesqram@gmail.com')

        print('---- Creating zone ----')

        zone1 = Zone.objects.create(name='Andalucía')

        print('---- Creating portfolio ----')

        portfolio1 = Portfolio.objects.create(artist=artist1, artisticName="Los rebujitos")
        portfolio1.zone.add(zone1)
        portfolio1.save()

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

    def test_driver_create_offer(self):

        print('Start test')
        data1 = {"username": "customer1", "password": "customer1customer1"}
        response = self.client.post("/api/login/", data1, format='json')

        token_num = response.get('x-auth')

        #Para evitar problemas si el token no existe en bd
        token = ''
        try:
            token = Token.objects.all().filter(pk=token_num).first().key
        except:
            pass
        # Data payload
        portfolio1 = Portfolio.objects.get(artisticName="Los rebujitos")
        payload = [
                # Test positivo, crear un calendar sin incidencias
                [token, ['2019-09-20'], portfolio1.id, 201]]#,
                # Test negativo - Fecha incorrecta
                #[token, 'Descripcion2', '2019 10:00:00', 1, portfolio1.id, 400],
                # Test negativo - Descripcion incorrecta
                #[token, '', '2019-05-10T10:00:00', 1, portfolio1.id, 400]]

        for data in payload:
            self.template_create_offer(data)

    def generateData(self, args):
        return {'days': args[1],
                'portfolio': args[2]}

    # Template function

    def template_create_offer(self, args):

        data = self.generateData(args)

        response_es = self.client.post('/offer/', data, format='json', HTTP_AUTHORIZATION='Token ' + args[0],
                                    HTTP_ACCEPT_LANGUAGE='es')

        self.assertEqual(args[-1], response_es.status_code)

        response_en = self.client.post('/offer/', data, format='json', HTTP_AUTHORIZATION='Token ' + args[0],
                                    HTTP_ACCEPT_LANGUAGE='en')

        self.assertEqual(args[-1], response_en.status_code)'''
