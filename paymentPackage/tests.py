from Grooving.models import Artist, Portfolio, User,  PaymentPackage, Customer, EventLocation, Zone, \
    Performance, SystemConfiguration, Fare, Custom
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.test import APITransactionTestCase


class PaymentPackageCreateTestCase(APITransactionTestCase):

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

        user2_artist10 = User.objects.create(username='artist2', password=make_password('artist2artist2'),
                                             first_name='Carlos', last_name='Campos Cuesta',
                                             email=your_email)

        artist2 = Artist.objects.create(user=user2_artist10, rating=5.0, phone='600304999',
                                        language='en',
                                        photo='https://img.discogs.com/jgyNBtPsY4DiLegwMrOC9N_yOc4=/600x600/smart/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/A-1452461-1423476836-6354.jpeg.jpg',
                                        iban='ES6621000418401234567891', paypalAccount='tamta.info@gmail.com')
        user3_artist10 = User.objects.create(username='artist3', password=make_password('artist3artist3'),
                                             first_name='Carlos', last_name='Campos Cuesta',
                                             email=your_email)

        artist3 = Artist.objects.create(user=user3_artist10, rating=5.0, phone='600304999',
                                        language='en',
                                        photo='https://img.discogs.com/jgyNBtPsY4DiLegwMrOC9N_yOc4=/600x600/smart/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/A-1452461-1423476836-6354.jpeg.jpg',
                                        iban='ES6621000418401234567891', paypalAccount='tamta.info@gmail.com')
        user4_artist10 = User.objects.create(username='artist4', password=make_password('artist4artist4'),
                                             first_name='Carlos', last_name='Campos Cuesta',
                                             email=your_email)

        artist4 = Artist.objects.create(user=user4_artist10, rating=5.0, phone='600304999',
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

        portfolio2 = Portfolio.objects.create(artist=artist2, artisticName="Los sinchanclas")
        portfolio2.zone.add(zone1)
        portfolio2.save()

        portfolio3 = Portfolio.objects.create(artist=artist3, artisticName="NFX")
        portfolio3.zone.add(zone1)
        portfolio3.save()

        portfolio4 = Portfolio.objects.create(artist=artist4, artisticName="AV7")
        portfolio4.zone.add(zone1)
        portfolio4.save()

        performance1 = Performance.objects.create(info="Informacion", hours=3, price=200)
        performance1.save()
        PaymentPackage.objects.create(description="Descripcion", currency="€", portfolio=portfolio3,
                                      performance=performance1)


        fare1 = Fare.objects.create(priceHour=25.0)
        fare1.save()
        PaymentPackage.objects.create(description='Fare Payment Package Type from Taylor Swift', portfolio=portfolio3,
                                      fare=fare1)


        custom1 = Custom.objects.create(minimumPrice=100.0)
        custom1.save()
        PaymentPackage.objects.create(description='Custom Payment Package Type from Rosalía', portfolio=portfolio3,
                                      custom=custom1)


        performance2 = Performance.objects.create(info="Informacion", hours=3, price=200)
        performance2.save()
        PaymentPackage.objects.create(description="Descripcion", currency="€", portfolio=portfolio4,
                                      performance=performance2)


        fare2 = Fare.objects.create(priceHour=25.0)
        fare2.save()
        PaymentPackage.objects.create(description='Fare Payment Package Type from Taylor Swift', portfolio=portfolio4,
                                      fare=fare2)


        custom2 = Custom.objects.create(minimumPrice=100.0)
        custom2.save()
        PaymentPackage.objects.create(description='Custom Payment Package Type from Rosalía', portfolio=portfolio4,
                                      custom=custom2)


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

    def test_driver_create_fare(self):

        print('---- Starting Create Fare tests ----')

        # Generate tokens

        bodyCustomer = {"username": "customer1", "password": "customer1customer1"}
        bodyArtist = {"username": "artist1", "password": "artist1artist1"}
        bodyArtist2 = {"username": "artist2", "password": "artist2artist2"}

        requestCustomer = self.client.post("/api/login/", bodyCustomer, format='json')
        requestArtist = self.client.post("/api/login/", bodyArtist, format='json')
        requestArtist2 = self.client.post("/api/login/", bodyArtist2, format='json')

        tokenCustomer = ''
        tokenArtist = ''
        tokenArtist2 = ''
        try:
            tokenCustomer = Token.objects.all().filter(pk=requestCustomer.get('x-auth')).first().key
            tokenArtist = Token.objects.all().filter(pk=requestArtist.get('x-auth')).first().key
            tokenArtist2 = Token.objects.all().filter(pk=requestArtist2.get('x-auth')).first().key
        except:
            print('---- Token doesn\'t retreive ----')

        # Data payload
        # ['Token', 'description', 'date', 'hours', 'price', paymentPackage_id', 'eventLocation_id']

        payload = [
                # POSITIVE TESTS
                # Fare with Integer Price
                [tokenArtist, 'Descripcion1', '100.0','es', 200],

                #NEGATIVE TESTS
                # Unauthenticated user
                ['', 'Descripcion1', '100.0','es', 401],
                # User unauthorized
                [tokenCustomer, 'Descripcion1', '100.0','es', 403],
                # Description not provided
                [tokenArtist, None, '100.0','es', 400],
                # Price not provided
                [tokenArtist, 'Descripcion1', None,'es', 400],
                # Negative Price provided
                [tokenArtist, 'Descripcion1', '-100.0','es', 400],
                # Price is 0
                [tokenArtist, 'Descripcion1', '0.0','es', 400],
                # Empty Description
                [tokenArtist, '', '100.0','es', 400],

                # POSITIVE TESTS
                # Fare with Integer Price
                [tokenArtist2, 'Descripcion1', '100.0','en', 200],

                # NEGATIVE TESTS
                # Unauthenticated user
                ['', 'Descripcion1', '100.0','en', 401],
                # User unauthorized
                [tokenCustomer, 'Descripcion1', '100.0','en', 403],
                # Description not provided
                [tokenArtist2, None, '100.0','en', 400],
                # Price not provided
                [tokenArtist2, 'Descripcion1', None,'en', 400],
                # Negative Price provided
                [tokenArtist2, 'Descripcion1', '-100.0','en', 400],
                # Price is 0
                [tokenArtist2, 'Descripcion1', '0.0','en', 400],
                # Empty Description
                [tokenArtist2, '', '100.0','en', 400]
        ]

        for data in payload:
            print('Payload index ' + str(payload.index(data)) + ': ' + str(data))
            self.template_create_fare(data)
            print('\n')

        print('---- Create Fare tests finished ----')

    def test_driver_create_custom(self):

        print('---- Starting Create Custom tests ----')

        # Generate tokens

        bodyCustomer = {"username": "customer1", "password": "customer1customer1"}
        bodyArtist = {"username": "artist1", "password": "artist1artist1"}
        bodyArtist2 = {"username": "artist2", "password": "artist2artist2"}

        requestCustomer = self.client.post("/api/login/", bodyCustomer, format='json')
        requestArtist = self.client.post("/api/login/", bodyArtist, format='json')
        requestArtist2 = self.client.post("/api/login/", bodyArtist2, format='json')

        tokenCustomer = ''
        tokenArtist = ''
        tokenArtist2 = ''
        try:
            tokenCustomer = Token.objects.all().filter(pk=requestCustomer.get('x-auth')).first().key
            tokenArtist = Token.objects.all().filter(pk=requestArtist.get('x-auth')).first().key
            tokenArtist2 = Token.objects.all().filter(pk=requestArtist2.get('x-auth')).first().key
        except:
            print('---- Token doesn\'t retreive ----')

        # Data payload
        # ['Token', 'description', 'date', 'hours', 'price', paymentPackage_id', 'eventLocation_id']

        payload = [
                # POSITIVE TESTS
                # Fare with Integer Price
                [tokenArtist, 'Descripcion1', '100.0','es', 200],

                #NEGATIVE TESTS
                # Unauthenticated user
                ['', 'Descripcion1', '100.0','es', 401],
                # User unauthorized
                [tokenCustomer, 'Descripcion1', '100.0','es', 404],
                # Description not provided
                [tokenArtist, None, '100.0','es', 400],
                # Price not provided
                [tokenArtist, 'Descripcion1', None,'es', 400],
                # Negative Price provided
                [tokenArtist, 'Descripcion1', '-100.0','es', 400],
                # Price is 0
                [tokenArtist, 'Descripcion1', '0.0','es', 400],
                # Empty Description
                [tokenArtist, '', '100.0','es', 400],

                # POSITIVE TESTS
                # Fare with Integer Price
                [tokenArtist2, 'Descripcion1', '100.0','en', 200],

                # NEGATIVE TESTS
                # Unauthenticated user
                ['', 'Descripcion1', '100.0','en', 401],
                # User unauthorized
                [tokenCustomer, 'Descripcion1', '100.0','en', 404],
                # Description not provided
                [tokenArtist2, None, '100.0','en', 400],
                # Price not provided
                [tokenArtist2, 'Descripcion1', None,'en', 400],
                # Negative Price provided
                [tokenArtist2, 'Descripcion1', '-100.0','en', 400],
                # Price is 0
                [tokenArtist2, 'Descripcion1', '0.0','en', 400],
                # Empty Description
                [tokenArtist2, '', '5.0','en', 400]
        ]

        for data in payload:
            print('Payload index ' + str(payload.index(data)) + ': ' + str(data))
            self.template_create_custom(data)
            print('\n')

        print('---- Create Custom tests finished ----')

    def test_driver_create_performance(self):

        print('---- Starting Create Performance tests ----')

        # Generate tokens

        bodyCustomer = {"username": "customer1", "password": "customer1customer1"}
        bodyArtist = {"username": "artist1", "password": "artist1artist1"}
        bodyArtist2 = {"username": "artist2", "password": "artist2artist2"}

        requestCustomer = self.client.post("/api/login/", bodyCustomer, format='json')
        requestArtist = self.client.post("/api/login/", bodyArtist, format='json')
        requestArtist2 = self.client.post("/api/login/", bodyArtist2, format='json')

        tokenCustomer = ''
        tokenArtist = ''
        tokenArtist2 = ''
        try:
            tokenCustomer = Token.objects.all().filter(pk=requestCustomer.get('x-auth')).first().key
            tokenArtist = Token.objects.all().filter(pk=requestArtist.get('x-auth')).first().key
            tokenArtist2 = Token.objects.all().filter(pk=requestArtist2.get('x-auth')).first().key
        except:
            print('---- Token doesn\'t retreive ----')

        # Data payload
        # ['Token', 'description', 'date', 'hours', 'price', paymentPackage_id', 'eventLocation_id']

        payload = [
                # POSITIVE TESTS
                # Fare with Integer Price
                [tokenArtist, 'Descripcion1', 'Info', '2','100.0','es', 200],

                #NEGATIVE TESTS
                # Unauthenticated user
                ['', 'Descripcion1', 'Info', '2','100.0','es', 401],
                # User unauthorized
                [tokenCustomer, 'Descripcion1', 'Info', '2','100.0','es', 403],
                # Price not provided
                [tokenArtist, 'Descripcion1','Info', '2', None,'es', 400],
                # Negative Price provided
                [tokenArtist, 'Descripcion1', 'Info', '2','-100.0','es', 400],
                # Price is 0
                [tokenArtist, 'Descripcion1', 'Info', '2','0.0','es', 400],

                # POSITIVE TESTS
                # Fare with Integer Price
                [tokenArtist2, 'Descripcion1', 'Info', '2','100.0','en', 200],

                # NEGATIVE TESTS
                # Unauthenticated user
                ['', 'Descripcion1', 'Info', '2','100.0','en', 401],
                # User unauthorized
                [tokenCustomer, 'Descripcion1', 'Info', '2','100.0','en', 403],
                # Price not provided
                [tokenArtist2, 'Descripcion1','Info', '2', None,'en', 400],
                # Negative Price provided
                [tokenArtist2, 'Descripcion1', 'Info', '2','-100.0','en', 400],
                # Price is 0
                [tokenArtist2, 'Descripcion1', 'Info', '2','0.0','en', 400],
        ]

        for data in payload:
            print('Payload index ' + str(payload.index(data)) + ': ' + str(data))
            self.template_create_performance(data)
            print('\n')

        print('---- Create Custom tests finished ----')

    def test_driver_edit_fare(self):

        print('---- Starting Create Fare tests ----')

        # Generate tokens

        bodyCustomer = {"username": "customer1", "password": "customer1customer1"}
        bodyArtist = {"username": "artist3", "password": "artist3artist3"}
        bodyArtist2 = {"username": "artist4", "password": "artist4artist4"}

        requestCustomer = self.client.post("/api/login/", bodyCustomer, format='json')
        requestArtist = self.client.post("/api/login/", bodyArtist, format='json')
        requestArtist2 = self.client.post("/api/login/", bodyArtist2, format='json')

        tokenCustomer = ''
        tokenArtist = ''
        tokenArtist2 = ''

        try:
            tokenCustomer = Token.objects.all().filter(pk=requestCustomer.get('x-auth')).first().key
            tokenArtist = Token.objects.all().filter(pk=requestArtist.get('x-auth')).first().key
            tokenArtist2 = Token.objects.all().filter(pk=requestArtist2.get('x-auth')).first().key
        except:
            print('---- Token doesn\'t retreive ----')

        artist3 = Artist.objects.get(user__username='artist3')
        fare1 = Fare.objects.get(paymentpackage__portfolio__artist=artist3)
        artist4 = Artist.objects.get(user__username='artist4')
        fare2 = Fare.objects.get(paymentpackage__portfolio__artist=artist4)

        # Data payload
        # ['Token', 'description', 'date', 'hours', 'price', paymentPackage_id', 'eventLocation_id']

        payload = [
                # POSITIVE TESTS
                # Fare with Integer Price
                [tokenArtist, 'Descripcion1', '100.0','es',fare1.id, 200],

                #NEGATIVE TESTS
                # Unauthenticated user
                ['', 'Descripcion1', '100.0','es',fare1.id, 401],
                # User unauthorized
                [tokenCustomer, 'Descripcion1', '100.0','es',fare1.id, 403],
                # Price not provided
                [tokenArtist, 'Descripcion1', None,'es',fare1.id, 400],
                # Negative Price provided
                [tokenArtist, 'Descripcion1', '-100.0','es',fare1.id, 400],
                # Price is 0
                [tokenArtist, 'Descripcion1', '0.0','es',fare1.id, 400],

                # POSITIVE TESTS
                # Fare with Integer Price
                [tokenArtist2, 'Descripcion1', '100.0','en',fare2.id, 200],

                # NEGATIVE TESTS
                # Unauthenticated user
                ['', 'Descripcion1', '5.0','en',fare1.id, 401],
                # User unauthorized
                [tokenCustomer, 'Descripcion1', '100.0','en',fare2.id, 403],
                # Price not provided
                [tokenArtist2, 'Descripcion1', None,'en',fare2.id, 400],
                # Negative Price provided
                [tokenArtist2, 'Descripcion1', '-100.0','en',fare2.id, 400],
                # Price is 0
                [tokenArtist2, 'Descripcion1', '0.0','en',fare2.id, 400]
        ]

        for data in payload:
            print('Payload index ' + str(payload.index(data)) + ': ' + str(data))
            self.template_edit_fare(data)
            print('\n')

        print('---- Create Fare tests finished ----')

    def test_driver_edit_custom(self):

        print('---- Starting Create Custom tests ----')

        # Generate tokens

        bodyCustomer = {"username": "customer1", "password": "customer1customer1"}
        bodyArtist = {"username": "artist3", "password": "artist3artist3"}
        bodyArtist2 = {"username": "artist4", "password": "artist4artist4"}

        requestCustomer = self.client.post("/api/login/", bodyCustomer, format='json')
        requestArtist = self.client.post("/api/login/", bodyArtist, format='json')
        requestArtist2 = self.client.post("/api/login/", bodyArtist2, format='json')

        tokenCustomer = ''
        tokenArtist = ''
        tokenArtist2 = ''
        try:
            tokenCustomer = Token.objects.all().filter(pk=requestCustomer.get('x-auth')).first().key
            tokenArtist = Token.objects.all().filter(pk=requestArtist.get('x-auth')).first().key
            tokenArtist2 = Token.objects.all().filter(pk=requestArtist2.get('x-auth')).first().key
        except:
            print('---- Token doesn\'t retreive ----')

        artist3 = Artist.objects.get(user__username='artist3')
        custom1 = Custom.objects.get(paymentpackage__portfolio__artist=artist3)
        artist4 = Artist.objects.get(user__username='artist4')
        custom2 = Custom.objects.get(paymentpackage__portfolio__artist=artist4)

        # Data payload
        # ['Token', 'description', 'date', 'hours', 'price', paymentPackage_id', 'eventLocation_id']

        payload = [
                # POSITIVE TESTS
                # Fare with Integer Price
                [tokenArtist, 'Descripcion1', '100.0','es',custom1.id, 200],

                #NEGATIVE TESTS
                # Unauthenticated user
                ['', 'Descripcion1', '5.0','es', 401],
                # User unauthorized
                [tokenCustomer, 'Descripcion1', '100.0','es',custom1.id, 403],
                # Price not provided
                [tokenArtist, 'Descripcion1', None,'es',custom1.id, 400],
                # Negative Price provided
                [tokenArtist, 'Descripcion1', '-5.0','es',custom1.id, 400],
                # Price is 0
                [tokenArtist, 'Descripcion1', '0.0','es',custom1.id, 400],

                # POSITIVE TESTS
                # Fare with Integer Price
                [tokenArtist2, 'Descripcion1', '100.0','en',custom2.id, 200],

                # NEGATIVE TESTS
                # Unauthenticated user
                ['', 'Descripcion1', '100.0','en',custom2.id, 401],
                # User unauthorized
                [tokenCustomer, 'Descripcion1', '100.0','en',custom2.id, 403],
                # Price not provided
                [tokenArtist2, 'Descripcion1', None,'en',custom2.id, 400],
                # Negative Price provided
                [tokenArtist2, 'Descripcion1', '-100.0','en',custom2.id, 400],
                # Price is 0
                [tokenArtist2, 'Descripcion1', '0.0','en',custom2.id, 400]
        ]

        for data in payload:
            print('Payload index ' + str(payload.index(data)) + ': ' + str(data))
            self.template_edit_custom(data)
            print('\n')

        print('---- Create Custom tests finished ----')

    def test_driver_edit_performance(self):

        print('---- Starting Create Performance tests ----')

        # Generate tokens

        bodyCustomer = {"username": "customer1", "password": "customer1customer1"}
        bodyArtist = {"username": "artist3", "password": "artist3artist3"}
        bodyArtist2 = {"username": "artist4", "password": "artist4artist4"}

        requestCustomer = self.client.post("/api/login/", bodyCustomer, format='json')
        requestArtist = self.client.post("/api/login/", bodyArtist, format='json')
        requestArtist2 = self.client.post("/api/login/", bodyArtist2, format='json')

        tokenCustomer = ''
        tokenArtist = ''
        tokenArtist2 = ''
        try:
            tokenCustomer = Token.objects.all().filter(pk=requestCustomer.get('x-auth')).first().key
            tokenArtist = Token.objects.all().filter(pk=requestArtist.get('x-auth')).first().key
            tokenArtist2 = Token.objects.all().filter(pk=requestArtist2.get('x-auth')).first().key
        except:
            print('---- Token doesn\'t retreive ----')

        #performance1 = Performance.objects.filter(paymentpackage=PaymentPackage.objects.filter(
            #portfolio=Portfolio.objects.filter(artist=requestArtist.json()['artist']['id']))).first()

        artist3 = Artist.objects.get(user__username = 'artist3')
        performance1 = Performance.objects.get(paymentpackage__portfolio__artist = artist3)
        artist4 = Artist.objects.get(user__username='artist4')
        performance2 = Performance.objects.get(paymentpackage__portfolio__artist = artist4)

        # Data payload
        # ['Token', 'description', 'date', 'hours', 'price', paymentPackage_id', 'eventLocation_id']

        payload = [
                # POSITIVE TESTS
                # Fare with Integer Price
                [tokenArtist, 'Descripcion1', 'Info', '2','100.0','es',performance1.id, 200],

                #NEGATIVE TESTS
                # Unauthenticated user
                ['', 'Descripcion1', 'Info', '2','100.0','es',performance1.id, 401],
                # User unauthorized
                [tokenCustomer, 'Descripcion1', 'Info', '2','100.0','es',performance1.id,403],
                # Price not provided
                [tokenArtist, 'Descripcion1','Info', '2', None,'es',performance1.id, 400],
                # Negative Price provided
                [tokenArtist, 'Descripcion1', 'Info', '2','-100.0','es',performance1.id, 400],
                # Price is 0
                [tokenArtist, 'Descripcion1', 'Info', '2','0.0','es',performance1.id, 400],

                # POSITIVE TESTS
                # Fare with Integer Price
                [tokenArtist2, 'Descripcion1', 'Info', '2','100.0','en',performance2.id, 200],

                # NEGATIVE TESTS
                # Unauthenticated user
                ['', 'Descripcion1', 'Info', '2','100.0','en',performance2.id, 401],
                # User unauthorized
                [tokenCustomer, 'Descripcion1', 'Info', '2','100.0','en',performance2.id, 403],
                # Price not provided
                [tokenArtist2, 'Descripcion1','Info', '2', None,'en',performance2.id, 400],
                # Negative Price provided
                [tokenArtist2, 'Descripcion1', 'Info', '2','-100.0','en',performance2.id, 400],
                # Price is 0
                [tokenArtist2, 'Descripcion1', 'Info', '2','0.0','en',performance2.id, 400],
        ]

        for data in payload:
            print('Payload index ' + str(payload.index(data)) + ': ' + str(data))
            self.template_edit_performance(data)
            print('\n')

        print('---- Create Custom tests finished ----')

    def generateData_Fare(self, args):
        return {'description': args[1],
                'priceHour': args[2]}

    def generateData_Custom(self, args):
        return {'description': args[1],
                'minimumPrice': args[2]}

    def generateData_Performance(self, args):
        return {'description': args[1],
                'info': args[2],
                'hours': args[3],
                'price': args[4]}

    # Template function

    def template_create_fare(self, args):

        data = self.generateData_Fare(args)

        response_es = self.client.post('/fare/', data, format='json', HTTP_AUTHORIZATION='Token ' + args[0],
                                    HTTP_ACCEPT_LANGUAGE=args[3])

        self.assertEqual(args[-1], response_es.status_code)

    def template_edit_fare(self, args):

        data = self.generateData_Fare(args)

        response_es = self.client.post('/fare/{}/'.format(str(args[4])), data, format='json', HTTP_AUTHORIZATION='Token ' + args[0],
                                    HTTP_ACCEPT_LANGUAGE=args[3])

        self.assertEqual(args[-1], response_es.status_code)

    def template_create_custom(self, args):

        data = self.generateData_Custom(args)

        response_es = self.client.post('/custom/', data, format='json', HTTP_AUTHORIZATION='Token ' + args[0],
                                    HTTP_ACCEPT_LANGUAGE=args[3])

        self.assertEqual(args[-1], response_es.status_code)

    def template_edit_custom(self, args):

        data = self.generateData_Custom(args)

        response_es = self.client.post('/custom/{}/'.format(str(args[4])), data, format='json', HTTP_AUTHORIZATION='Token ' + args[0],
                                    HTTP_ACCEPT_LANGUAGE=args[3])

        self.assertEqual(args[-1], response_es.status_code)

    def template_create_performance(self, args):

        data = self.generateData_Performance(args)

        response_es = self.client.post('/performance/', data, format='json', HTTP_AUTHORIZATION='Token ' + args[0],
                                    HTTP_ACCEPT_LANGUAGE=args[5])

        self.assertEqual(args[-1], response_es.status_code)

    def template_edit_performance(self, args):

        data = self.generateData_Performance(args)

        response_es = self.client.post('/performance/{}/'.format(str(args[6])), data, format='json', HTTP_AUTHORIZATION='Token ' + args[0],
                                    HTTP_ACCEPT_LANGUAGE=args[5])

        self.assertEqual(args[-1], response_es.status_code)
