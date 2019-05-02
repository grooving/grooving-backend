from Grooving.models import Artist, Portfolio, User,  PaymentPackage, Customer, EventLocation, Zone, \
    Performance, SystemConfiguration, Fare, Custom
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

        artist1 = Artist.objects.create(user=user1_artist10, rating=5.0, phone='600304999',
                                        language='en',
                                        photo='https://img.discogs.com/jgyNBtPsY4DiLegwMrOC9N_yOc4=/600x600/smart/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/A-1452461-1423476836-6354.jpeg.jpg',
                                        iban='ES6621000418401234567891', paypalAccount='tamta.info@gmail.com')

        user2_customer1 = User.objects.create(username='customer1', password=make_password('customer1customer1'),
                                              first_name='Rafael', last_name='Esquivias Ramírez',
                                              email=your_email)

        customer1 = Customer.objects.create(user=user2_customer1, phone='639154189', holder='Rafael Esquivias Ramírez',
                                            expirationDate='2020-10-01', number='4651001401188232',
                                            language='en',
                                            paypalAccount='rafesqram@gmail.com')

        zone1 = Zone.objects.create(name='Andalucía')

        EventLocation.objects.create(name="Sala Custom", address="C/Madrid",
                                                       equipment="Speakers and microphone",
                                                       description="The best event location",
                                                       zone=zone1, customer_id=customer1.id)

        user3_customer2 = User.objects.create(username='customer2', password=make_password('customer2customer2'),
                                              first_name='Rafael', last_name='Esquivias Ramírez',
                                              email=your_email)

        customer2 = Customer.objects.create(user=user3_customer2, phone='639154189', holder='Rafael Esquivias Ramírez',
                                            expirationDate='2020-10-01', number='4651001401188232',
                                            language='en',
                                            paypalAccount='rafesqram@gmail.com')

        zone2 = Zone.objects.create(name='Madrid')

        EventLocation.objects.create(name="Sala Custom", address="C/Madrid",
                                       equipment="Speakers and microphone",
                                       description="The best event location",
                                       zone=zone2, customer_id=customer2.id)

        portfolio1 = Portfolio.objects.create(artist=artist1, artisticName="Los rebujitos")
        portfolio1.zone.add(zone1)
        portfolio1.save()

        performance1 = Performance.objects.create(info="Informacion", hours=3, price=200)
        PaymentPackage.objects.create(description="Descripcion", currency="€", portfolio=portfolio1,
                                        performance=performance1)

        fare1 = Fare.objects.create(priceHour=25.0)
        PaymentPackage.objects.create(description='Fare Payment Package Type from Taylor Swift', portfolio=portfolio1,
                                        fare=fare1)

        custom1 = Custom.objects.create(minimumPrice=100.0)
        PaymentPackage.objects.create(description='Custom Payment Package Type from Rosalía', portfolio=portfolio1,
                                        custom=custom1)

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

        print('---- Starting Create Offer tests ----')

        # Generate tokens

        bodyCustomer = {"username": "customer1", "password": "customer1customer1"}
        bodyArtist = {"username": "artist1", "password": "artist1artist1"}

        requestCustomer = self.client.post("/api/login/", bodyCustomer, format='json')
        requestArtist = self.client.post("/api/login/", bodyArtist, format='json')

        tokenCustomer = ''
        tokenArtist = ''
        try:
            tokenCustomer = Token.objects.all().filter(pk=requestCustomer.get('x-auth')).first().key
            tokenArtist = Token.objects.all().filter(pk=requestArtist.get('x-auth')).first().key
        except:
            print('---- Token doesn\'t retreive ----')

        # References

        eventLocation1 = EventLocation.objects.filter(customer__user__username='customer1').first()
        eventLocation2 = EventLocation.objects.filter(customer__user__username='customer2').first()
        performancePackage = PaymentPackage.objects.filter(performance__isnull=False).first()
        farePackage = PaymentPackage.objects.filter(fare__isnull=False).first()
        customPackage = PaymentPackage.objects.filter(custom__isnull=False).first()

        # Data payload
        # ['Token', 'description', 'date', 'hours', 'price', paymentPackage_id', 'eventLocation_id']

        payload = [
                # POSITIVE TESTS
                # Offer with Performanace package
                [tokenCustomer, 'Descripcion1', '2019-05-11T10:00:00', None, None, performancePackage.id, eventLocation1.id, 201],
                # Offer with Fare package
                [tokenCustomer, 'Descripcion2', '2019-05-12T10:00:00', 3.5, None, farePackage.id, eventLocation1.id, 201],
                # Offer with Custom package
                [tokenCustomer, 'Descripcion3', '2019-05-13T10:00:00', 3.5, 1000.0, customPackage.id, eventLocation1.id, 201],

                #NEGATIVE TESTS
                # Unauthenticated user
                ['', 'Descripcion1', '2019-05-10T10:00:00', None, None, performancePackage.id, eventLocation1.id, 401],
                # User unauthorized
                [tokenArtist, 'Descripcion1', '2019-05-10T10:00:00', None, None, performancePackage.id, eventLocation1.id, 403],
                # Description not provided
                [tokenCustomer, None, '2019-05-10T10:00:00', None, None, performancePackage.id, eventLocation1.id, 400],
                # Date not provided
                [tokenCustomer, 'Descripcion1', None, None, None, performancePackage.id, eventLocation1.id, 400],
                # Date bad provided
                [tokenCustomer, 'Descripcion1', '2019-05-10', None, None, performancePackage.id, eventLocation1.id, 400],
                # Past date
                [tokenCustomer, 'Descripcion1', '2018-05-10T10:00:00', None, None, performancePackage.id, eventLocation1.id, 400],
                # Payment package not provided
                [tokenCustomer, 'Descripcion1', '2018-05-10T10:00:00', None, None, None, eventLocation1.id, 400],
                # Payment package not exist
                [tokenCustomer, 'Descripcion1', '2018-05-10T10:00:00', None, None, 999, eventLocation1.id, 400],
                # Fare package - hours not provided
                [tokenCustomer, 'Descripcion1', '2018-05-10T10:00:00', None, None, farePackage.id, eventLocation1.id, 400],
                # Fare package - hours bad provided
                [tokenCustomer, 'Descripcion1', '2018-05-10T10:00:00', None, 1.3, farePackage.id, eventLocation1.id, 400],
                # Custom package - price not provided
                [tokenCustomer, 'Descripcion1', '2018-05-10T10:00:00', None, None, customPackage.id, eventLocation1.id, 400],
                # Custom package - price below minimum
                [tokenCustomer, 'Descripcion1', '2018-05-10T10:00:00', 10.0, None, customPackage.id, eventLocation1.id, 400],
                # Event location not provided
                [tokenCustomer, 'Descripcion1', '2018-05-10T10:00:00', None, None, performancePackage.id, None, 400],
                # Event location not exist
                [tokenCustomer, 'Descripcion1', '2018-05-10T10:00:00', None, None, performancePackage.id, 999, 400],
                # Event location not belong to user
                [tokenCustomer, 'Descripcion1', '2018-05-10T10:00:00', None, None, performancePackage.id, eventLocation2.id, 400],
        ]

        for data in payload:
            print('Payload index ' + str(payload.index(data)) + ': ' + str(data))
            self.template_create_offer(data)
            print('\n')

        print('---- Create Offer tests finished ----')

    def generateData(self, args):
        return {'description': args[1],
                'date': args[2],
                'hours': args[3],
                'price': args[4],
                'paymentPackage_id': args[5],
                'eventLocation_id': args[6]}

    # Template function

    def template_create_offer(self, args):

        data = self.generateData(args)

        response_es = self.client.post('/offer/', data, format='json', HTTP_AUTHORIZATION='Token ' + args[0],
                                    HTTP_ACCEPT_LANGUAGE='es')

        self.assertEqual(args[-1], response_es.status_code)

        response_en = self.client.post('/offer/', data, format='json', HTTP_AUTHORIZATION='Token ' + args[0],
                                    HTTP_ACCEPT_LANGUAGE='en')

        self.assertEqual(args[-1], response_en.status_code)
