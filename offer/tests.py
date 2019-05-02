from Grooving.models import Artist, Portfolio, User,  PaymentPackage, Customer, EventLocation, Zone, \
    Performance, SystemConfiguration, Fare, Custom, Offer, Transaction
from .serializers import OfferSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.test import APITransactionTestCase


class OfferTestCase(APITransactionTestCase):

    def setUp(self):
        your_email = 'utri1990@gmail.com'
        print('-------- Setup test --------')

        print('---- Creating user test ----')

        user1_artist1 = User.objects.create(username='artist1', password=make_password('artist1artist1'),
                                             first_name='Carlos', last_name='Campos Cuesta',
                                             email=your_email)

        artist1 = Artist.objects.create(user=user1_artist1, rating=5.0, phone='600304999',
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

        event_location1 = EventLocation.objects.create(name="Sala Custom", address="C/Madrid",
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

        event_location2 = EventLocation.objects.create(name="Sala Custom", address="C/Madrid",
                                       equipment="Speakers and microphone",
                                       description="The best event location",
                                       zone=zone2, customer_id=customer2.id)

        portfolio1 = Portfolio.objects.create(artist=artist1, artisticName="Los rebujitos")
        portfolio1.zone.add(zone1)
        portfolio1.save()

        performance1 = Performance.objects.create(info="Informacion", hours=3, price=200)
        performancePackage = PaymentPackage.objects.create(description="Descripcion", currency="€", portfolio=portfolio1,
                                        performance=performance1)

        fare1 = Fare.objects.create(priceHour=25.0)
        farePackage = PaymentPackage.objects.create(description='Fare Payment Package Type from Taylor Swift', portfolio=portfolio1,
                                        fare=fare1)

        custom1 = Custom.objects.create(minimumPrice=100.0)
        customPackage = PaymentPackage.objects.create(description='Custom Payment Package Type from Rosalía', portfolio=portfolio1,
                                        custom=custom1)

        transaction1 = Transaction.objects.create(paypalArtist='carlosdj.espectaculos@gmail.com',
                                                        braintree_id='4578eph3', amount="120")

        transaction2 = Transaction.objects.create(paypalArtist='carlosdj.espectaculos@gmail.com',
                                                        braintree_id='ew0ayqav', amount='120')
        transaction3 = Transaction.objects.create(paypalArtist='carlosdj.espectaculos@gmail.com',
                                                        braintree_id='50vckfr9', amount='120')

        Offer.objects.create(description='Oferta 1 to Carlos DJ by performance',
                             status='CONTRACT_MADE',
                             date='2019-04-29 12:00:00', hours=2.5, price='120', currency='EUR',
                             appliedVAT=7, paymentPackage=performancePackage,
                             eventLocation=event_location1, transaction=transaction1,
                             paymentCode='qwertyasdf')

        Offer.objects.create(description='Oferta 2 to Carlos DJ by performance',
                             status='PAYMENT_MADE',
                             date='2019-07-25 12:00:00', hours=1.5, price='120', currency='EUR',
                             paymentCode='0123456789',
                             appliedVAT=7, paymentPackage=performancePackage,
                             eventLocation=event_location2, transaction=transaction2)

        Offer.objects.create(description='Oferta 5 to Carlos DJ by fare', status='PENDING',
                             date='2019-10-25 12:00:00', hours=1.5, price='120', currency='EUR',
                             appliedVAT=7, paymentPackage=farePackage,
                             eventLocation=event_location1, transaction=transaction3)

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

    #### 2.9 HIRE AN ARTIST ####

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
        # ['Token', 'description', 'date', 'hours', 'price', paymentPackage_id', 'eventLocation_id', 'http_code']

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

    def generateDataCreateOffer(self, args):
        return {'description': args[1],
                'date': args[2],
                'hours': args[3],
                'price': args[4],
                'paymentPackage_id': args[5],
                'eventLocation_id': args[6]}

    def generateDataBraintree(self, id_offer, nonce='fake-valid-nonce'):
        return {'payment_method_nonce': nonce,
                'id_offer': id_offer}

    def template_create_offer(self, args):

        dataCreateOffer = self.generateDataCreateOffer(args)

        response_create_offer_es = self.client.post('/offer/', dataCreateOffer, format='json', HTTP_AUTHORIZATION='Token ' + args[0],
                                    HTTP_ACCEPT_LANGUAGE='es')

        self.assertEqual(args[-1], response_create_offer_es.status_code)

        serialized_es = OfferSerializer(data=response_create_offer_es.data, partial=True)

        dataBraintree_es = self.generateDataBraintree(serialized_es.initial_data.get('id'), 'fake-valid-nonce')

        response_braintree_es = self.client.post('/braintree_token/', dataBraintree_es, format='json', HTTP_AUTHORIZATION='Token ' + args[0],
                                    HTTP_ACCEPT_LANGUAGE='es')

        response_create_offer_en = self.client.post('/offer/', dataCreateOffer, format='json', HTTP_AUTHORIZATION='Token ' + args[0],
                                    HTTP_ACCEPT_LANGUAGE='en')

        self.assertEqual(args[-1], response_create_offer_en.status_code)

        serialized_en = OfferSerializer(data=response_create_offer_en.data, partial=True)

        dataBraintree_en = self.generateDataBraintree(serialized_en.initial_data.get('id'), 'fake-valid-nonce')

        response_braintree_en = self.client.post('/braintree_token/', dataBraintree_en, format='json',
                                                 HTTP_AUTHORIZATION='Token ' + args[0],
                                                 HTTP_ACCEPT_LANGUAGE='en')

    #### END ####

    #### 2.10 & 2.11 WITHDRAW/REJECTED OFFER ####

    def test_driver_withdraw_rejected_offer(self):

        print('---- Starting Withdraw/Rejected Offer tests ----')

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


        # Data payload
        # ['Token', 'status', 'reason', 'http_code']

        payload = [
                # POSITIVE TESTS
                # Withdrawn offer as customer
                [tokenCustomer, 'WITHDRAWN', 'This is a reason', 200],
                # Rejected offer as artist
                [tokenArtist, 'REJECTED', 'This is a reason', 200],

                #NEGATIVE TESTS
                # Unauthenticated user
                ['', 'WITHDRAWN', 'This is a reason', 401],
                # User unauthorized
                [tokenArtist, 'WITHDRAWN', 'This is a reason', 400],
                # Status not provided
                [tokenCustomer, None, 'This is a reason', 400],
                # Status bad provided
                [tokenCustomer, '', 'This is a reason', 400],
                # Status non accepted
                [tokenCustomer, 'HOLA', 'This is a reason', 400],
                # Reason not provided
                [tokenCustomer, 'WITHDRAWN', None, 400],
                # Reason bad provided
                [tokenCustomer, 'WITHDRAWN', '', 400]
        ]

        for data in payload:
            print('Payload index ' + str(payload.index(data)) + ': ' + str(data))
            self.template_withdraw_customer(data)
            print('\n')

        print('---- Withdraw/Rejected Offer tests finished ----')

    def generateDataWithdrawCustomer(self, args):
        return {'status': args[1],
                'reason': args[2]}

    def template_withdraw_customer(self, args):

        dataWithdrawOffer = self.generateDataWithdrawCustomer(args)

        offer = Offer.objects.filter(status='PENDING').first()

        response_withdraw_customer_es = self.client.put('/offer/'+str(offer.id)+'/', dataWithdrawOffer, format='json', HTTP_AUTHORIZATION='Token ' + args[0],
                                    HTTP_ACCEPT_LANGUAGE='es')

        self.assertEqual(args[-1], response_withdraw_customer_es.status_code)

        offer.status = 'PENDING'
        offer.reason = None
        offer.save()

        response_withdraw_customer_en = self.client.put('/offer/'+str(offer.id)+'/', dataWithdrawOffer, format='json', HTTP_AUTHORIZATION='Token ' + args[0],
                                    HTTP_ACCEPT_LANGUAGE='en')

        self.assertEqual(args[-1], response_withdraw_customer_en.status_code)

        offer.status = 'PENDING'
        offer.reason = None
        offer.save()


    #### END ####

    #### 2.12 ACCEPT AN OFFER AS A ARTIST ####

    def test_driver_accept_offer(self):

        print('---- Starting Accept Offer tests ----')

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

        # Data payload
        # ['Token', 'status', 'reason', 'http_code']

        payload = [
            # POSITIVE TESTS
            # Accept offer as artist
            [tokenArtist, 'CONTRACT_MADE', 200],

            # NEGATIVE TESTS
            # Unauthenticated user
            ['', 'CONTRACT_MADE', 401],
            # User unauthorized
            [tokenArtist, 'CONTRACT_MADE', 400],
            # Status not provided
            [tokenArtist, None, 400],
            # Status bad provided
            [tokenArtist, '', 400],
            # Status non accepted
            [tokenArtist, 'HOLA', 400]
        ]

        for data in payload:
            print('Payload index ' + str(payload.index(data)) + ': ' + str(data))
            self.template_accept_offer(data)
            print('\n')

        print('---- Withdraw/Rejected Offer tests finished ----')

    def generateDataAcceptOffer(self, args):
        return {'status': args[1]}

    def template_accept_offer(self, args):

        dataAcceptOffer = self.generateDataAcceptOffer(args)

        offer = Offer.objects.filter(status='PENDING').first()

        response_accept_offer_es = self.client.put('/offer/' + str(offer.id) + '/', dataAcceptOffer,
                                                        format='json', HTTP_AUTHORIZATION='Token ' + args[0],
                                                        HTTP_ACCEPT_LANGUAGE='es')

        self.assertEqual(args[-1], response_accept_offer_es.status_code)

        offer.status = 'PENDING'
        offer.save()
        offer.transaction.paypalArtist = None
        offer.transaction.braintree_id = None
        offer.transaction.save()

        response_accept_offer_en = self.client.put('/offer/' + str(offer.id) + '/', dataAcceptOffer,
                                                        format='json', HTTP_AUTHORIZATION='Token ' + args[0],
                                                        HTTP_ACCEPT_LANGUAGE='en')

        self.assertEqual(args[-1], response_accept_offer_en.status_code)

        offer.status = 'PENDING'
        offer.save()
        offer.transaction.paypalArtist = None
        offer.transaction.braintree_id = None
        offer.transaction.save()

    #### END ####


