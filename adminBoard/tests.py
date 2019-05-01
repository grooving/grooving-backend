from Grooving.models import  Artist, Portfolio, User,  PaymentPackage, Customer, EventLocation, Zone, \
    Performance, SystemConfiguration,Admin
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.test import APITransactionTestCase


class ZoneTestCase(APITransactionTestCase):

    def setUp(self):
        your_email = 'utri1990@gmail.com'
        print('-------- Setup test --------')

        print('---- Creating user test ----')

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
        zone_lvl1_spain = Zone.objects.create(name="España", parentZone=None)
        zone_lvl1_spain.save()

        zone_lvl2_andalucia = Zone.objects.create(name="Andalucia", parentZone=zone_lvl1_spain)
        zone_lvl2_andalucia.save()
        zone_lvl2_aragon = Zone.objects.create(name="Aragón", parentZone=zone_lvl1_spain)
        zone_lvl2_aragon.save()

        zone_lvl3_sevilla = Zone.objects.create(name="Sevilla", parentZone=zone_lvl2_andalucia)
        zone_lvl3_sevilla.save()

        zone_lvl3_cordoba = Zone.objects.create(name="Cordoba", parentZone=zone_lvl2_andalucia)
        zone_lvl3_cordoba.save()

        zone_lvl3_zaragoza = Zone.objects.create(name="Zaragoza", parentZone=zone_lvl2_aragon)
        zone_lvl3_zaragoza.save()

        zone_lvl3_teruel = Zone.objects.create(name="Teruel", parentZone=zone_lvl2_aragon)
        zone_lvl3_teruel.save()

    # Driver function

    def test_driver_create_zone(self):

        print('Start test')
        data1 = {"username": "admin", "password": "admin"}
        response = self.client.post("/api/admin/login/", data1, format='json')

        token_num = response.get('x-auth')

        #Para evitar problemas con el token si no existiera
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

                # Test positivo, crear una zona con padre lvl 1
                [token, 'Comunidad Valenciana', spain_id,'es', 201],
                # Test positivo, crear una zona con padre lvl 2
                [token, 'Huelva', andalucia_id,'es', 201],
                # Test negativo, crear una zona sin padre
                [token, 'Perro',None,'es', 400],
                # Test negativo, crear una zona sin estar logueado
                ['390494jdididij', 'Inglaterra', andalucia_id,'es', 401],
                # Test negativo, crear una zona de lvl4
                [token, 'Morón de la frontera', sevilla_id,'es', 400],
                # Test negativo, crear una zona ya existente
                [token, 'Sevilla', andalucia_id, 'es', 400],

        ]

        for data in payload:
            self.template_create_zone(data)

    def generateData(self, args):
        return {'name': args[1],
                'parentZone': args[2]}

    # Template function

    def template_create_zone(self, args):

        data = self.generateData(args)

        response_es = self.client.post('/admin/zone/', data, format='json', HTTP_AUTHORIZATION='Token ' + args[0],
                                    HTTP_ACCEPT_LANGUAGE=args[3])

        self.assertEqual(args[-1], response_es.status_code)

