from Grooving.models import  Artist, Portfolio, User,  PaymentPackage, Customer, EventLocation, Zone, \
    Performance, SystemConfiguration
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.test import APITransactionTestCase


class OfferTestCase(APITransactionTestCase):

    def setUp(self):
        your_email = 'utri1990@gmail.com'
        print('-------- Setup test --------')

        print('---- Creating user test ----')

        user1_artist10 = User.objects.create(username='artist1', password=make_password('artist1artist1'),
                                             first_name='Carlos', last_name='Campos Cuesta',
                                             email=your_email)
        Token.objects.create(user=user1_artist10)

        artist1 = Artist.objects.create(user=user1_artist10, rating=5.0, phone='600304999',
                                        language='en',
                                        photo='https://img.discogs.com/jgyNBtPsY4DiLegwMrOC9N_yOc4=/600x600/smart/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/A-1452461-1423476836-6354.jpeg.jpg',
                                        iban='ES6621000418401234567891', paypalAccount='tamta.info@gmail.com')

        user2_customer1 = User.objects.create(username='customer1', password=make_password('customer1customer1'),
                                              first_name='Rafael', last_name='Esquivias Ramírez',
                                              email=your_email)
        Token.objects.create(user=user2_customer1)

        customer1 = Customer.objects.create(user=user2_customer1, phone='639154189', holder='Rafael Esquivias Ramírez',
                                            expirationDate='2020-10-01', number='4651001401188232',
                                            language='en',
                                            paypalAccount='rafesqram@gmail.com')

        zone1 = Zone.objects.create(name='Andalucía')

        event_location1 = EventLocation.objects.create(name="Sala Custom", address="C/Madrid",
                                                       equipment="Speakers and microphone",
                                                       description="The best event location",
                                                       zone=zone1, customer_id=customer1.id)

        event_location1.save()

        portfolio1 = Portfolio.objects.create(artist=artist1, artisticName="Los rebujitos")
        portfolio1.zone.add(zone1)
        portfolio1.save()

        performance1 = Performance.objects.create(info="Informacion", hours=3, price=200)
        payment_package1 = PaymentPackage.objects.create(description="Descripcion", currency="€", portfolio=portfolio1,
                                                         performance=performance1)
        payment_package1.save()

        performance1.save()

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

        # Data payload
        portfolio1 = Portfolio.objects.get(artisticName="Los rebujitos")
        payload = [
                # Test positivo, crear oferta a un PERFORMANCE package
                ['customer1', 'Descripcion1', '2019-05-10T10:00:00', 1, portfolio1.id, 201],
                # Test negativo - Fecha incorrecta
                ['customer1', 'Descripcion2', '2019 10:00:00', 1, portfolio1.id, 400],
                # Test negativo - Descripcion incorrecta
                ['customer1', '', '2019-05-10T10:00:00', 1, portfolio1.id, 400]]

        for data in payload:
            self.template_create_offer(data)

    def generateData(self, args):
        return {'description': args[1],
                'date': args[2],
                'paymentPackage_id': args[3],
                'eventLocation_id': args[4]}

    # Template function

    def template_create_offer(self, args):

        # Get user to make request
        user = User.objects.get(username=args[0])
        if user is None:
            raise Exception('Unknown username')

        data = self.generateData(args)

        response_es = self.client.post('/offer/', data, format='json',HTTP_AUTHORIZATION='Token ' + str(user.auth_token),
                                    HTTP_ACCEPT_LANGUAGE='es')

        self.assertEqual(args[-1], response_es.status_code)

        response_en = self.client.post('/offer/', data, format='json', HTTP_AUTHORIZATION='Token ' + str(user.auth_token),
                                    HTTP_ACCEPT_LANGUAGE='en')

        self.assertEqual(args[-1], response_en.status_code)
