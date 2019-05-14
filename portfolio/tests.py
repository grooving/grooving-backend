from Grooving.models import  Artist, Portfolio, User,  PaymentPackage, Customer, EventLocation, Zone, \
    Performance, SystemConfiguration,Admin, ArtisticGender
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.test import APITransactionTestCase


class PortfolioTestCase(APITransactionTestCase):

    def setUp(self):
        your_email = 'utri1990@gmail.com'
        print('-------- Setup test --------')

        print('---- Creating Portfolio Tests ----')

        user3_admin = User.objects.create(id=1, username='admin', password=make_password('admin'), is_staff=True,
                                           is_superuser=True, first_name='Chema', last_name='Alonso',
                                           email="grupogrooving@gmail.com")
        user3_admin.save()
        admin = Admin.objects.create(pk=1, user=user3_admin, language='es')
        admin.save()
        user1_artist10 = User.objects.create(pk=2, username='artist1', password=make_password('artist1artist1'),
                                             first_name='Carlos', last_name='Campos Cuesta',
                                             email=your_email)
        Token.objects.create(user=user1_artist10)

        artist1 = Artist.objects.create(pk=1, user=user1_artist10, rating=5.0, phone='600304999',
                                        language='en',
                                        photo='https://img.discogs.com/jgyNBtPsY4DiLegwMrOC9N_yOc4=/600x600/smart/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/A-1452461-1423476836-6354.jpeg.jpg',
                                        iban='ES6621000418401234567891', paypalAccount='tamta.info@gmail.com')

        user1_artist2 = User.objects.create(pk=3, username='artist2', password=make_password('artist2artist2'),
                                            first_name='Pablo', last_name='Motos',
                                            email=your_email)
        Token.objects.create(user=user1_artist2)

        artist2 = Artist.objects.create(pk=2, user=user1_artist2, rating=5.0, phone='600304999',
                                        language='en',
                                        photo='https://img.discogs.com/jgyNBtPsY4DiLegwMrOC9N_yOc4=/600x600/smart/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/A-1452461-1423476836-6354.jpeg.jpg',
                                        iban='ES6621000418401234567891', paypalAccount='tamta.info@gmail.com')



        user2_customer1 = User.objects.create(pk=4, username='customer1', password=make_password('customer1customer1'),
                                              first_name='Rafael', last_name='Esquivias Ramírez',
                                              email=your_email)
        Token.objects.create(user=user2_customer1)

        customer1 = Customer.objects.create(pk=1, user=user2_customer1, phone='639154189', holder='Rafael Esquivias Ramírez',
                                            expirationDate='2020-10-01', number='4651001401188232',
                                            language='en',
                                            paypalAccount='rafesqram@gmail.com')

        zone1 = Zone.objects.create(pk=1, name='Murcia')

        zone2 = Zone.objects.create(pk=2, name='Sevilla')

        event_location1 = EventLocation.objects.create(name="Sala Custom", address="C/Madrid",
                                                       equipment="Speakers and microphone",
                                                       description="The best event location",
                                                       zone=zone1, customer_id=customer1.id)

        event_location1.save()

        portfolio1 = Portfolio.objects.create(pk=1, artist=artist1, artisticName="Los rebujitos",biography="Biografia")
        portfolio1.zone.add(zone1)
        portfolio1.save()

        performance1 = Performance.objects.create(info="Informacion", hours=3, price=200)
        payment_package1 = PaymentPackage.objects.create(description="Descripcion", currency="€", portfolio=portfolio1,
                                                         performance=performance1)
        payment_package1.save()

        performance1.save()

        artisticGenre = ArtisticGender.objects.create(pk=1, name_es="Rock", name_en="Rock")


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

        print('---- Starting Portfolio tests ----')
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

        artist1 = Artist.objects.get(pk=1)

        portfolio = Portfolio.objects.get(pk=1)

        artisticGenreValido = ArtisticGender.objects.get(pk=1)

        zone = Zone.objects.get(pk=1)

        artisticGenreNoValido = "Orégano"

        artisticNameNoValido = ""

        artisticNameNuevo = "Ya no somos los rebujitos"

        portfoliomoduleVideoValido = "https://www.youtube.com/watch?v=Psv5dmrs3U0"

        portfoliomoduleImagenValida = "https://images.pexels.com/photos/1108099/pexels-photo-1108099.jpg"

        portfoliomoduleVideoNoValido = "Ejemplo"

        portfoliomoduleImagenNoValida = "Lalala"

        bannerValido = "https://images.pexels.com/photos/1108099/pexels-photo-1108099.jpg"

        bannerNoValido = "Imagen"

        mainPhotoValida = "https://images.pexels.com/photos/1108099/pexels-photo-1108099.jpg"

        mainPhotoNoValida = "SoyUnaImagennoValida"

        portfoliomoduleBiography = "Patata"

        payload = [

                # TESTS EN ESPAÑOL
                # Token, id portfolio, artistic name, biography, banner, images, videos, main_photo, artistic genres, zones, idioma, HTTP response

                # Test positivo, editar un artistic name
                [token, portfolio.id, artisticNameNuevo, portfolio.biography, portfolio.banner, [portfoliomoduleImagenValida], [portfoliomoduleVideoValido], portfoliomoduleImagenValida, [], [], artist1.id, 'es', 200],
                # Test positivo, editar biografía
                [token, portfolio.id, portfolio.artisticName, portfoliomoduleBiography, portfolio.banner, [portfoliomoduleImagenValida], [portfoliomoduleVideoValido], portfoliomoduleImagenValida, [], [], artist1.id, 'es', 200],
                # Test positivo, editar banner
                [token, portfolio.id, portfolio.artisticName, portfolio.biography, bannerValido, [portfoliomoduleImagenValida], [portfoliomoduleVideoValido], portfoliomoduleImagenValida, [], [], artist1.id, 'es', 200],
                # Test positivo, editar imagenes
                [token, portfolio.id, portfolio.artisticName, portfolio.biography, portfolio.banner, [portfoliomoduleImagenValida], [portfoliomoduleVideoValido], portfoliomoduleImagenValida, [], [], artist1.id, 'es', 200],
                # Test positivo, editar videos
                [token, portfolio.id, portfolio.artisticName, portfolio.biography, portfolio.banner, [portfoliomoduleImagenValida], [portfoliomoduleVideoValido], portfoliomoduleImagenValida, [], [], artist1.id, 'es', 200],
                # Test positivo, editar main photo
                [token, portfolio.id, portfolio.artisticName, portfolio.biography, portfolio.banner, [portfoliomoduleImagenValida], [portfoliomoduleVideoValido], portfoliomoduleImagenValida, [], [], artist1.id, 'es', 200],
                 # Test positivo, cambiar artist genres
                [token, portfolio.id, artisticNameNuevo, portfolio.biography, portfolio.banner, [portfoliomoduleImagenValida], [portfoliomoduleVideoValido], portfoliomoduleImagenValida, [artisticGenreValido.name_es], [], artist1.id, 'es', 200],
                # Test positivo, editar zones
                [token, portfolio.id, artisticNameNuevo, portfolio.biography, portfolio.banner, [portfoliomoduleImagenValida], [portfoliomoduleVideoValido], portfoliomoduleImagenValida, [], [zone.name], artist1.id, 'es', 200],

                #Test positivo 1, artistic name vacío

                [token, portfolio.id, '', portfolio.biography, portfolio.banner,
                [portfoliomoduleImagenValida], [portfoliomoduleVideoValido], portfoliomoduleImagenValida, [], [],
                artist1.id, 'es', 200],

                #Test negativo 2, banner con url inavlida

                [token, portfolio.id, artisticNameNuevo, portfolio.biography, bannerNoValido,
                [portfoliomoduleImagenValida], [portfoliomoduleVideoValido], portfoliomoduleImagenValida, [], [],
                artist1.id, 'es', 400],

                #Test negativo 3, imagen con url inavlida

                [token, portfolio.id, artisticNameNuevo, portfolio.biography, portfolio.banner,
                [portfoliomoduleImagenNoValida], [portfoliomoduleVideoValido], portfoliomoduleImagenValida, [], [],
                artist1.id, 'es', 400],

                #Test negativo 4, video invalido

                [token, portfolio.id, artisticNameNuevo, portfolio.biography, portfolio.banner,
                [portfoliomoduleImagenValida], [portfoliomoduleVideoNoValido], portfoliomoduleImagenValida, [], [],
                artist1.id, 'es', 400],

                #Test negativo 5, main photo inválida

                [token, portfolio.id, artisticNameNuevo, portfolio.biography, portfolio.banner,
                [portfoliomoduleImagenValida], [portfoliomoduleVideoValido], portfoliomoduleImagenNoValida, [], [],
                artist1.id, 'es', 400],

                #Test 6, genre inexistente

                [token, portfolio.id, artisticNameNuevo, portfolio.biography, portfolio.banner,
                [portfoliomoduleImagenValida], [portfoliomoduleVideoValido], portfoliomoduleImagenValida, ['Country'], [],
                artist1.id, 'es', 400],

                #Test 7, zone inexistente

                [token, portfolio.id, artisticNameNuevo, portfolio.biography, portfolio.banner,
                [portfoliomoduleImagenValida], [portfoliomoduleVideoValido], portfoliomoduleImagenValida, [], ['París'],
                artist1.id, 'es', 400],

                # TESTS EN INGLES

                # Test positivo, editar un artistic name
                [token, portfolio.id, artisticNameNuevo, portfolio.biography, portfolio.banner,
                [portfoliomoduleImagenValida], [portfoliomoduleVideoValido], portfoliomoduleImagenValida, [], [],
                artist1.id, 'en', 200],
                # Test positivo, editar biografía
                [token, portfolio.id, portfolio.artisticName, portfoliomoduleBiography, portfolio.banner,
                [portfoliomoduleImagenValida], [portfoliomoduleVideoValido], portfoliomoduleImagenValida, [], [],
                artist1.id, 'en', 200],
                # Test positivo, editar banner
                [token, portfolio.id, portfolio.artisticName, portfolio.biography, bannerValido,
                [], [portfoliomoduleVideoValido], portfoliomoduleImagenValida, [], [],
                artist1.id, 'en', 200],
                # Test positivo, editar imagenes
                [token, portfolio.id, portfolio.artisticName, portfolio.biography, portfolio.banner,
                [portfoliomoduleImagenValida], [portfoliomoduleVideoValido], portfoliomoduleImagenValida, [], [],
                artist1.id, 'en', 200],
                # Test positivo, editar videos
                [token, portfolio.id, portfolio.artisticName, portfolio.biography, portfolio.banner,
                [portfoliomoduleImagenValida], [portfoliomoduleVideoValido], portfoliomoduleImagenValida, [], [],
                artist1.id, 'en', 200],
                # Test positivo, editar main photo
                [token, portfolio.id, portfolio.artisticName, portfolio.biography, portfolio.banner,
                [portfoliomoduleImagenValida], [portfoliomoduleVideoValido], portfoliomoduleImagenValida, [], [],
                artist1.id, 'en', 200],
                # Test positivo, cambiar artist genres
                [token, portfolio.id, artisticNameNuevo, portfolio.biography, portfolio.banner,
                [portfoliomoduleImagenValida], [portfoliomoduleVideoValido], portfoliomoduleImagenValida,
                [artisticGenreValido.name_es], [], artist1.id, 'en', 200],
                # Test positivo, editar zones
                [token, portfolio.id, artisticNameNuevo, portfolio.biography, portfolio.banner,
                [portfoliomoduleImagenValida], [portfoliomoduleVideoValido], portfoliomoduleImagenValida, [], [zone.name],
                artist1.id, 'en', 200],

                # Test positivo, artistic name vacío

                [token, portfolio.id, '', portfolio.biography, portfolio.banner,
                [portfoliomoduleImagenValida], [portfoliomoduleVideoValido], portfoliomoduleImagenValida, [], [],
                artist1.id, 'en', 200],

                # Test negativo 2, banner con url inavlida

                [token, portfolio.id, artisticNameNuevo, portfolio.biography, bannerNoValido,
                [portfoliomoduleImagenValida], [portfoliomoduleVideoValido], portfoliomoduleImagenValida, [], [],
                artist1.id, 'en', 400],

                # Test negativo 3, imagen con url inavlida

                [token, portfolio.id, artisticNameNuevo, portfolio.biography, portfolio.banner,
                [portfoliomoduleImagenNoValida], [portfoliomoduleVideoValido], portfoliomoduleImagenValida, [], [],
                artist1.id, 'en', 400],

                # Test negativo 4, video invalido

                [token, portfolio.id, artisticNameNuevo, portfolio.biography, portfolio.banner,
                [portfoliomoduleImagenValida], [portfoliomoduleVideoNoValido], portfoliomoduleImagenValida, [], [],
                artist1.id, 'en', 400],

                # Test negativo 5, main photo inválida

                [token, portfolio.id, artisticNameNuevo, portfolio.biography, portfolio.banner,
                [portfoliomoduleImagenValida], [portfoliomoduleVideoValido], portfoliomoduleImagenNoValida, [], [],
                artist1.id, 'en', 400],

                # Test 6, genre inexistente

                [token, portfolio.id, artisticNameNuevo, portfolio.biography, portfolio.banner,
                [portfoliomoduleImagenValida], [portfoliomoduleVideoValido], portfoliomoduleImagenValida, ['Country'], [],
                artist1.id, 'en', 400],

                # Test 7, zone inexistente

                [token, portfolio.id, artisticNameNuevo, portfolio.biography, portfolio.banner,
                [portfoliomoduleImagenValida], [portfoliomoduleVideoValido], portfoliomoduleImagenValida, [], ['París'],
                artist1.id, 'en', 400],

        ]

        for data in payload:
            print("---> Test " + str(payload.index(data)+1))
            self.template_edit_portfolio(data)

    def generateData(self, args):
        return {'id': args[1],
                'artisticName': args[2],
                'biography': args[3],
                'banner': args[4],
                'images': args[5],
                'videos': args[6],
                'main_photo': args[7],
                'artisticGenders': args[8],
                'zone': args[9]
                }

    # Template function

    def template_edit_portfolio(self, args):

        data = self.generateData(args)

        response_create = self.client.put('/portfolio/{}/'.format(str(args[1])), data, format='json', HTTP_AUTHORIZATION='Token ' + args[0],
                                    HTTP_ACCEPT_LANGUAGE=args[-2])

        self.assertEqual(args[-1], response_create.status_code)
