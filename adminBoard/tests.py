from Grooving.models import  Artist, Portfolio, User,  PaymentPackage, Customer, EventLocation, Zone, \
    Performance, SystemConfiguration,Admin
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.test import APITransactionTestCase


class ZoneTestCase(APITransactionTestCase):

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
        zone_lvl1_spain = Zone.objects.create(name="España", parentZone=None)
        zone_lvl1_spain.save()

        zone_lvl2_andalucia = Zone.objects.create(name="Andalucia", parentZone=zone_lvl1_spain)
        zone_lvl2_andalucia.save()
        zone_lvl2_aragon = Zone.objects.create(name="Aragón", parentZone=zone_lvl1_spain)
        zone_lvl2_aragon.save()

        zone_lvl2_galicia = Zone.objects.create(name="Galicia", parentZone=zone_lvl1_spain)
        zone_lvl2_galicia.save()

        zone_lvl3_sevilla = Zone.objects.create(name="Sevilla", parentZone=zone_lvl2_andalucia)
        zone_lvl3_sevilla.save()

        zone_lvl3_cordoba = Zone.objects.create(name="Cordoba", parentZone=zone_lvl2_andalucia)
        zone_lvl3_cordoba.save()

        zone_lvl3_zaragoza = Zone.objects.create(name="Zaragoza", parentZone=zone_lvl2_aragon)
        zone_lvl3_zaragoza.save()

        zone_lvl3_teruel = Zone.objects.create(name="Teruel", parentZone=zone_lvl2_aragon)
        zone_lvl3_teruel.save()

        zone_lvl3_lugo = Zone.objects.create(name="Lugo", parentZone=zone_lvl2_galicia)
        zone_lvl3_lugo.save()

        zone_lvl3_pontevedra = Zone.objects.create(name="Pontevedra", parentZone=zone_lvl2_galicia)
        zone_lvl3_pontevedra.save()

    def test_driver_create_zone(self):

        print('---- Starting Zone tests ----')
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
        payload = [

                # TESTS EN ESPAÑOL
                # Token, Nombre de la zona, zona padre, language, mensaje HTTP

                # Test positivo, crear una zona con padre lvl 1
                [token, 'Comunidad Valenciana', spain_id,'es', 201],
                # Test positivo, crear una zona con padre lvl 2
                [token, 'Huelva', andalucia_id,'es', 201],
                # Test negativo, crear una zona sin padre
                [token, 'Perro',None,'es', 400],
                # Test negativo, crear una zona sin estar logueado
                ['390494jdididij', 'Inglaterra', andalucia_id,'es', 401],
                # Test negativo, crear una zona de lvl4
                [token, 'Morón de la frontera', sevilla_id, 'es', 400],
                # Test negativo, crear una zona ya existente
                [token, 'Sevilla', andalucia_id, 'es', 400],
                 # Test negativo, id que no está en base de datos
                [token, 'Sevilla', 50, 'es', 400],
                # Test negativo, id None
                [token, 'Sevilla', None, 'es', 400],

            # TESTS EN INGLES
                # Test positivo, crear una zona con padre lvl 1
                [token, 'Comunidat Valenciana', spain_id, 'en', 201],
                # Test positivo, crear una zona con padre lvl 2
                [token, 'Cadiz', andalucia_id, 'en', 201],
                # Test negativo, crear una zona sin padre
                [token, 'Perro', None, 'es', 400],
                # Test negativo, crear una zona sin estar logueado
                ['390494jdididij', 'Inglaterra', andalucia_id, 'en', 401],
                # Test negativo, crear una zona de lvl4
                [token, 'Morón de la frontera', sevilla_id, 'en', 400],
                # Test negativo, crear una zona ya existente
                [token, 'Sevilla', andalucia_id, 'en', 400],
                # Test negativo, idioma no permitido
                [token, 'Galicia', spain_id, 'catalan', 400],
                # Test negativo, id que no está en base de datos
                [token, 'Sevilla', 50, 'en', 400],
                # Test negativo, id None
                [token, 'Sevilla', None, 'en', 400],

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


    def test_driver_get_statistics(self):

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


        data2 = {"username": "artist1", "password": "artist1artist1"}
        response = self.client.post("/api/login/", data2, format='json')

        token_num2 = response.get('x-auth')

        # Para evitar problemas con el token si no existiera
        token2 = ''
        try:
            token2 = Token.objects.all().filter(pk=token_num2).first().key
        except:
            pass
        # Data payload

        payload = [

            # Token, language, mensaje HTTP
            # Test positivo get statistics español
            [token, 'es',200],
            # Test positivo get statistics español
            [token2, 'es', 403],
            # Test positivo get statistics inglés
            [token, 'en', 200],
            # Test positivo get statistics español
            [token2, 'en', 403],

        ]

        for data in payload:
            print("---> Test " + str(payload.index(data) + 1))
            self.template_get_statistics(data)

        # Template function

    def template_get_statistics(self, args):

        response_delete = self.client.get('/admin/statistics/',HTTP_AUTHORIZATION='Token ' + args[0],
                                             HTTP_ACCEPT_LANGUAGE=args[1])

        self.assertEqual(args[-1], response_delete.status_code)