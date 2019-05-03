
from Grooving.models import  Artist, Portfolio, User,  PaymentPackage, Customer, EventLocation, Zone, \
    Performance, SystemConfiguration,Admin,Transaction,Offer
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.test import APITransactionTestCase
from populate import _service_generate_unique_payment_code

class ChatTestCase(APITransactionTestCase):

    def setUp(self):
        your_email = 'utri1990@gmail.com'
        print('-------- Setup test --------')

        print('---- Creating Zone Tests ----')

        user3_admin = User.objects.create(username='admin', password=make_password('admin'), is_staff=True,
                                          is_superuser=True, first_name='Chema', last_name='Alonso',
                                          email="grupogrooving@gmail.com")
        user3_admin.save()
        admin = Admin.objects.create(user=user3_admin, language='es')
        admin.save()
        user1_artist10 = User.objects.create(username='artist1', password=make_password('artist1artist1'),
                                             first_name='Carlos', last_name='Campos Cuesta',
                                             email=your_email)
        Token.objects.create(user=user1_artist10)

        artist1 = Artist.objects.create(user=user1_artist10, rating=5.0, phone='600304999',
                                        language='en',
                                        photo='https://img.discogs.com/jgyNBtPsY4DiLegwMrOC9N_yOc4=/600x600/smart/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/A-1452461-1423476836-6354.jpeg.jpg',
                                        iban='ES6621000418401234567891', paypalAccount='tamta.info@gmail.com')

        user3_artist2 = User.objects.create(username='artist2', password=make_password('artist2artist2'),
                                             first_name='Antonio', last_name='LopezJimenez',
                                             email='carlos@gmail.com')
        Token.objects.create(user=user3_artist2)

        Artist.objects.create(user=user3_artist2, rating=5.0, phone='600304999',
                                        language='en',
                                        photo='https://img.discogs.com/jgyNBtPsY4DiLegwMrOC9N_yOc4=/600x600/smart/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/A-1452461-1423476836-6354.jpeg.jpg',
                                        iban='ES6621000418401234567891', paypalAccount='artist2.info@gmail.com')

        user2_customer1 = User.objects.create(username='customer1', password=make_password('customer1customer1'),
                                              first_name='Rafael', last_name='Esquivias Ramírez',
                                              email=your_email)
        Token.objects.create(user=user2_customer1)

        customer1 = Customer.objects.create(user=user2_customer1, phone='639154189', holder='Rafael Esquivias Ramírez',
                                            expirationDate='2020-10-01', number='4651001401188232',
                                            language='en',
                                            paypalAccount='rafesqram@gmail.com')

        zone1 = Zone.objects.create(name='Murcia')

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

        transaction_offer1 = Transaction.objects.create(paypalArtist='carlosdj.espectaculos@gmail.com',
                                                        braintree_id='4578eph3', amount="120")
        transaction_offer1.save()  # CONTRACT_MADE - OK

        offer1_performance1 = Offer.objects.create(description='Oferta 1 Test',
                                                   status='CONTRACT_MADE',
                                                   date='2019-04-29 12:00:00', hours=5, price='70', currency='EUR',
                                                   appliedVAT=7, paymentPackage=payment_package1,
                                                   eventLocation=event_location1, transaction=transaction_offer1,
                                                   paymentCode=_service_generate_unique_payment_code())
        offer1_performance1.save()

    def test_driver_get_chat(self):

        print('---- Starting Zone tests ----')
        data1 = {"username": "artist1", "password": "artist1artist1"}
        response = self.client.post("/api/login/", data1, format='json')

        token_num = response.get('x-auth')

        # Para evitar problemas con el token si no existiera
        token = ''
        try:
            token = Token.objects.all().filter(pk=token_num).first().key

        except:
            pass

        data2 = {"username": "artist2", "password": "artist22artist22"}
        response2 = self.client.post("/api/login/", data2, format='json')

        token_num2 = response2.get('x-auth')

        # Para evitar problemas con el token si no existiera
        token2 = ''
        try:
            token2 = Token.objects.all().filter(pk=token_num2).first().key

        except:
            pass

        data2 = {"username": "customer1", "password": "customer1customer1"}
        response3 = self.client.post("/api/login/", data2, format='json')

        token_num3 = response3.get('x-auth')

        # Para evitar problemas con el token si no existiera
        token3 = ''
        try:
            token3 = Token.objects.all().filter(pk=token_num3).first().key

        except:
            pass
        # Data payload

        offer1_id = Offer.objects.get(description="Oferta 1 Test").id
        payload = [

            # TESTS EN ESPAÑOL
            # Test positivo, get chat como artista dueño de la oferta
            [token, offer1_id, 'es', 200],
            # Test positivo, get chat como customer dueño de la oferta
            [token3, offer1_id, 'es', 200],
            # Test negativo, get chat de una oferta que no es tuya
            [token2, offer1_id, 'es', 401],
            # Test negativo, get chat de una oferta que no existe
            [token, 40, 'es', 403],
            # Test negativo, get chat de una oferta que no existe
            [token, None, 'es', 404],

            #TESTS EN INGLÉS
            # Test positivo, get chat como artista dueño de la oferta
            [token, offer1_id, 'en', 200],
            # Test positivo, get chat como customer dueño de la oferta
            [token3, offer1_id, 'en', 200],
            # Test negativo, get chat de una oferta que no es tuya
            [token2, offer1_id, 'en', 401],
            # Test negativo, get chat de una oferta que no existe
            [token, 40, 'en', 403],



        ]

        for data in payload:
            print("---> Test " + str(payload.index(data) + 1))
            self.template_get_chat(data)


    # Template function

    def template_get_chat(self, args):

        response_create = self.client.get('/chat/{}/'.format(args[1]), format='json', HTTP_AUTHORIZATION='Token ' + args[0],
                                           HTTP_ACCEPT_LANGUAGE=args[2])

        self.assertEqual(args[-1], response_create.status_code)