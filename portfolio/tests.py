from Grooving.models import  Artist, Portfolio, User,  PaymentPackage, Customer, EventLocation, Zone, \
    Performance, SystemConfiguration,Admin, ArtisticGender
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.test import APITransactionTestCase


class ZoneTestCase(APITransactionTestCase):

    def setUp(self):
        your_email = 'utri1990@gmail.com'
        print('-------- Setup test --------')

        print('---- Creating Portfolio Tests ----')

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

        user1_artist2 = User.objects.create(username='artist2', password=make_password('artist2artist2'),
                                            first_name='Pablo', last_name='Motos',
                                            email=your_email)
        Token.objects.create(user=user1_artist2)

        artist2 = Artist.objects.create(user=user1_artist2, rating=5.0, phone='600304999',
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

        zone1 = Zone.objects.create(name='Murcia')

        zone2 = Zone.objects.create(name='Sevilla')

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

        artisticGenre = ArtisticGender.objects.create("Rock", None)


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

    def test_driver_edit_portfolio(self):

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
        # Data payload
        portfolio = Portfolio.objects.get(artisticName="Los rebujitos")

        artisticGenreValido = ArtisticGender.objects.get(name="Rock")

        zone = Zone.objects.get(name="Sevilla")

        artisticGenreNoValido = "Orégano"

        artisticNameNoValido = ""

        artisticNameNuevo = "Ya no somos los rebujitos"

        portfoliomoduleVideoValido = "https://www.youtube.com/watch?v=Psv5dmrs3U0"

        portfoliomoduleImagenValida = "https://images.pexels.com/photos/1108099/pexels-photo-1108099.jpeg"

        portfoliomoduleVideoNoValido = "Ejemplo"

        portfoliomoduleImagenNoValida = "Lalala"

        bannerValido = "https://images.pexels.com/photos/1108099/pexels-photo-1108099.jpeg"

        bannerNoValido = "Imagen"

        mainPhotoValida = "https://images.pexels.com/photos/1108099/pexels-photo-1108099.jpeg"

        mainPhotoNoValida = "SoyUnaImagennoValida"

        portfoliomoduleBiography = "Patata"

        payload = [

                # TESTS EN ESPAÑOL
                # Token, id portfolio, artistic name, biography, banner, images, videos, main_photo, artistic genres, zones, HTTP response

                # Test positivo, editar un artistic name
                [token, portfolio.id, artisticNameNuevo, portfolio.biography, portfolio.banner, [], [], '', [], 'es', 200],
                # Test positivo, editar biografía
                [token, portfolio.id, portfolio.artisticName, portfoliomoduleBiography, portfolio.banner, [], [], '', [], [], 'es', 200],
                # Test positivo, editar banner
                [token, portfolio.id, portfolio.artisticName, portfolio.biography, bannerValido, [], [], '', [], [], 'es', 200],
                # Test positivo, editar imagenes
                [token, portfolio.id, artisticNameNuevo, '', '', [portfoliomoduleImagenValida], [], [], '', [], 'es', 200],
                # Test positivo, editar videos
                [token, portfolio.id, artisticNameNuevo, '', '', [], [portfoliomoduleVideoValido], '', [], [], 'es', 200],
                # Test positivo, editar main photo
                [token, portfolio.id, artisticNameNuevo, '', '', [], [], '', [], [], 'es', 200],
                 # Test positivo, cambiar artist genres
                [token, portfolio.id, artisticNameNuevo, '', '', [], [], '', [artisticNameNoValido], [], 'es', 200],
                # Test positivo, editar zones
                [token, portfolio.id, artisticNameNuevo, '', '', [], [], '', [], [zone], 'es', 200],

            # TESTS EN INGLES


        ]

        for data in payload:
            print("---> Test " + str(payload.index(data)+1))
            self.template_create_zone(data)

    def generateData(self, args):
        return {'name': args[1],
                'parentZone': args[2]}

    # Template function

    def template_create_zone(self, args):

        data = self.generateData(args)

        response_create = self.client.post('/admin/zone/', data, format='json', HTTP_AUTHORIZATION='Token ' + args[0],
                                    HTTP_ACCEPT_LANGUAGE=args[3])

        self.assertEqual(args[-1], response_create.status_code)

    #TEST EDIT ZONE

    def test_driver_edit_zone(self):

        print('Start test')
        data1 = {"username": "admin", "password": "admin"}
        response = self.client.post("/api/admin/login/", data1, format='json')

        token_num = response.get('x-auth')

        # Para evitar problemas con el token si no existiera
        token = ''
        try:
            token = Token.objects.all().filter(pk=token_num).first().key
        except:
            pass
        # Data payload

        spain_id = Zone.objects.get(name='España').id
        andalucia_id = Zone.objects.get(name='Andalucia').id
        sevilla_id = Zone.objects.get(name='Sevilla').id
        cordoba_id = Zone.objects.get(name='Cordoba').id
        galicia_id = Zone.objects.get(name='Galicia').id
        teruel_id = Zone.objects.get(name='Teruel').id
        murcia_id = Zone.objects.get(name='Murcia').id
        payload = [

                # TESTS EN ESPAÑOL
                # Token, Nombre de la zona, zona padre, zona que se edita, language, mensaje HTTP

                # Test positivo, editar una zona con padre lvl 1
                [token, 'Comunidad Valenciana', spain_id,sevilla_id,'es', 200],
                # Test positivo, editar una zona con padre lvl 2
                [token, 'Sevilia', andalucia_id,sevilla_id,'es', 200],
                # Test negativo, editar una zona sin padre
                [token, 'Perro', None, sevilla_id, 'es', 400],
                # Test negativo, editar una zona sin estar logueado
                ['390494jdididij', 'Inglaterra', andalucia_id,sevilla_id,'es', 401],
                # Test negativo, editar una zona y ponerla en lvl4
                [token, 'Morón de la frontera', sevilla_id,galicia_id,'es', 400],

                # Test negativo, id de parent zone que no está en base de datos
                [token, 'Sevilla', 50,sevilla_id,'es', 400],
                # Test negativo, id de parent zone None
                 [token, 'Sevilla', None,sevilla_id, 'es', 400],
                # Test negativo, id de zone inexistente
                [token, 'Sevilla', andalucia_id, 50, 'es', 404],
                # Test negativo, id de zone None
                [token, 'Sevilla', andalucia_id, None, 'es', 400],

                #TESTS EN INGLES
                # Test positivo, editar una zona con padre lvl 1
                [token, 'Comunidat Valenciana', spain_id, sevilla_id, 'en', 200],
                # Test positivo, editar una zona con padre lvl 2
                [token, 'Cadiz', andalucia_id, sevilla_id, 'en', 200],
                # Test negativo, editar una zona sin padre
                [token, 'Perro', None, sevilla_id, 'en', 400],
                # Test negativo, editar una zona sin estar logueado
                ['390494jdididij', 'Inglaterra', andalucia_id, sevilla_id, 'en', 401],
                # Test negativo, editar una zona y ponerla en lvl4
                [token, 'Morón de la frontera', teruel_id, cordoba_id, 'en', 400],
                # Test negativo, id de zone inexistente
                [token, 'Sevilla', 50, sevilla_id, 'en', 400],
                # Test negativo, id de zone None
                [token, 'Sevilla', None, sevilla_id, 'en', 400],


                # Test negativo, idioma no permitido
                [token, 'Comunitate Valenciana', spain_id, sevilla_id, 'cat', 400],


        ]

        for data in payload:
            print("---> Test " + str(payload.index(data) + 1))
            self.template_edit_zone(data)

    # Template function

    def template_edit_zone(self, args):

        data = self.generateData(args)
        response_edit = self.client.put('/admin/zone/{}/'.format(str(args[3])), data, format='json', HTTP_AUTHORIZATION='Token ' + args[0],
                                    HTTP_ACCEPT_LANGUAGE=args[4])

        self.assertEqual(args[-1], response_edit.status_code)

    def test_driver_delete_zone(self):

        print('Start test')
        data1 = {"username": "admin", "password": "admin"}
        response = self.client.post("/api/admin/login/", data1, format='json')

        token_num = response.get('x-auth')

        # Para evitar problemas con el token si no existiera
        token = ''
        try:
            token = Token.objects.all().filter(pk=token_num).first().key
        except:
            pass
        # Data payload

        andalucia_id = Zone.objects.get(name='Andalucia').id
        sevilla_id = Zone.objects.get(name='Sevilla').id
        spain_id = Zone.objects.get(name='España').id
        # Murcia pertenece a un event location de un artista
        murcia_id = Zone.objects.get(name='Murcia').id
        payload = [

            # Token, zona que se borra, language, mensaje HTTP

            # Test negativo, borrar una zona sin estar logueado
            ['390494jdididij', sevilla_id, 'es', 401],
            # Test negativo español, borrar una zona que pertenece a un event location de un artista
            [token, murcia_id, 'es', 400],
            # Test negativo inglés, borrar una zona que pertenece a un event location de un artista
            [token, murcia_id, 'en', 400],
            # Test negativo, eliminar una zona con id inexistente
            [token, 'Sevilla', andalucia_id, 50, 'es', 400],
            # Test negativo, eliminar zona con id None
            [token, 'Sevilla', andalucia_id, None, 'es', 400],

            # Test positivo, eliminar una zona lvl 3
            [token, sevilla_id, 'es', 200],
            # Test positivo, eliminar una zona  lvl 2
            [token, andalucia_id, 'es', 200],
            # Test positivo, eliminar una zona  lvl 1
            [token, spain_id, 'es', 200],



        ]

        for data in payload:
            print("---> Test " + str(payload.index(data) + 1))
            self.template_delete_zone(data)

        # Template function

    def template_delete_zone(self, args):

        data = self.generateData(args)
        response_delete = self.client.delete('/admin/zone/{}/'.format(str(args[1])), data, format='json',
                                        HTTP_AUTHORIZATION='Token ' + args[0],
                                        HTTP_ACCEPT_LANGUAGE=args[2])

        self.assertEqual(args[-1], response_delete.status_code)