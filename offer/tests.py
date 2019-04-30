from twisted.conch.test.test_transport import factory

from Grooving.models import Offer, Artist, Portfolio, User, Calendar, PaymentPackage, Customer, EventLocation, Zone, \
    Performance, Fare, Custom, SystemConfiguration
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from django.test import TestCase
from rest_framework.exceptions import APIException
from rest_framework.authtoken.serializers import AuthTokenSerializer
from login.views import LoginManager
from . import views
import json
import datetime
import pytz

your_email = 'utri1990@gmail.com'


class OfferTestCase(APITestCase):

    def setUp(self):
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

        portfolio1 = Portfolio.objects.create(artist=artist1, artisticName="Los rebujitos")
        portfolio1.zone.add(zone1)
        portfolio1.save()

    def tearDown(self):
        print('Rollback')

    # Driver function

    def test_driver_create_offer(self):
        print('Start test')

        # Data payload

        payload = [['customer1', 'dasdadadssd', '2019-05-10T10:00:00', 10, 1, 200],
                   ['customer1', '200'],
                   ['customer1', '200']]

        for data in payload:
            try:
                # Call template function
                self.template_create_offer(data)
            except Exception as e:
                print("ERROR:\n" + "Index payload: " + str(payload.index(data)) + "\n" + "Exception: " + e.args[0])

    def generateBody(self, args):
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

        try:
            # factory = APIRequestFactory()

            # request_login = factory.post('/api/login/', login_body, content_type='application/json')
            # response_login = LoginManager.post(request=request_login)
            #
            # if response_login.has_header('x-auth'):
            #     token = response_login.__getitem__('x-auth')
            # else:
            #     raise APIException('Bad login')

            data = self.generateBody(args)

            request_offer = self.client.post('/offer/', data, format='json',
                                             HTTP_AUTHORIZATION='Token ' + str(user.auth_token))

            # response_offer = views.CreateOffer.post(request=request_offer)

            self.assertEqual(args[-1], request_offer.status_code)

        except Exception as e:
            self.assertEqual(args[-1], e.status_code)

# def test_manage_offer_artist(self):
#
#     print("TEST_MANAGE_OFFER_ARTIST\n")
#
#     days = ['2019-06-02', '2019-08-02', '2019-10-15', '2019-11-02']
#     date = datetime.datetime(2020,2,7,8,49,56,81433, pytz.UTC)
#
#     user1_artist1 = User.objects.create(username='artist1', password=make_password('artist1artist1'),
#                                         first_name='Cdds', last_name='Pedro',
#                                         email='artist1@gmail.com')
#     user1_artist1.save()
#
#     user1_customer1 = User.objects.create(username='customer1', password=make_password('customer1customer1'),
#                                           first_name='Cdds', last_name='Pedro',
#                                           email='customer1@gmail.com')
#     user1_customer1.save()
#     zone1 = Zone.objects.create(name="Sevilla Sur")
#     zone1.save()
#
#     customer1 = Customer.objects.create(holder="customer1", expirationDate=date, user=user1_customer1,
#                                         number=9393393939393)
#
#     customer1.save()
#     event_location1 = EventLocation.objects.create(name="Sala Rajoy", address="C/Madrid",
#                                                    equipment="Speakers and microphone",
#                                                    description="The best event location",
#                                                    zone=zone1, customer_id=customer1.id)
#     event_location1.save()
#     portfolio1 = Portfolio.objects.create(artisticName="Juanartist")
#     portfolio1.zone.add(zone1)
#     portfolio1.save()
#
#     artist1 = Artist.objects.create(user=user1_artist1, portfolio=portfolio1, phone='600304999')
#     artist1.save()
#
#     performance1 = Performance.objects.create(info="info", hours=3, price=200.0)
#     performance1.save()
#     payment_package1 = PaymentPackage.objects.create(description="Paymentcription",
#                                                      portfolio=portfolio1, performance=performance1)
#
#     payment_package1.save()
#
#     calendar1 = Calendar.objects.create(days=days, portfolio=portfolio1)
#     calendar1.save()
#
#     offer1 = Offer.objects.create(description="DESCRIPTIONOFFER1", status='PENDING', date=date, price="200",
#                                   hours=2, paymentCode='EEE', eventLocation=event_location1,
#                                   paymentPackage=payment_package1, appliedVAT="0.35")
#     offer1.save()
#
#     data1 = {"username": "artist1", "password": "artist1artist1"}
#     response = self.client.post("/api/login/", data1, format='json')
#
#     token_num = response.get('x-auth')
#     token = Token.objects.all().filter(pk=token_num).first()
#     print(token.key)
#     self.assertEqual(response.status_code, 200)
#
#     data = {"status": "CONTRACT_MADE"}
#
#     response1 = self.client.put('/offer/{}/'.format(offer1.id), data, format='json',
#                                 HTTP_AUTHORIZATION='Token '+token.key)
#     #self.assertEqual(response1.status_code, 200)
#     print(response1)
#
#     data1 = {"status": "CANCELED"}
#
#     response2 = self.client.put('/offer/{}/'.format(offer1.id), data1, format='json',
#                                 HTTP_AUTHORIZATION='Token ' + token.key)
#     #self.assertEqual(response2.status_code, 200)
#
#     data2 = {"username": "customer1", "password": "customer1customer1"}
#     response3 = self.client.post("/api/login/", data2, format='json')
#     token_num2 = response3.get('x-auth')
#     token2 = Token.objects.all().filter(pk=token_num2).first()
#     self.assertEqual(response3.status_code, 200)
#     offer1.status = "PENDING"
#     offer1.save()
#     print("\n\n")
#     data3 = {"status": "WITHDRAWN"}
#
#     response4 = self.client.put('/offer/{}/'.format(offer1.id), data3, format='json',
#                                 HTTP_AUTHORIZATION='Token ' + token2.key)
#     self.assertEqual(response4.status_code, 200)
#
#     offer1.status = "CONTRACT_MADE"
#     offer1.save()
#     data4 = {"status": "CANCELED"}
#     response5 = self.client.put('/offer/{}/'.format(offer1.id), data4, format='json',
#                                 HTTP_AUTHORIZATION='Token ' + token2.key)
#     #self.assertEqual(response5.status_code, 200)
#
#     offer1.status = "CONTRACT_MADE"
#     offer1.save()
#
#     response6 = self.client.get('/paymentCode/?offer={}'.format(offer1.id),
#                                 HTTP_AUTHORIZATION='Token ' + token2.key)
#
#     print(response)
#     self.assertEqual(response6.status_code, 200)
#
#     offer1.status = "CANCELED"
#     offer1.save()
#
#     response7 = self.client.get('/paymentCode/?offer={}'.format(offer1.id),
#                                 HTTP_AUTHORIZATION='Token ' + token2.key)
#     self.assertEqual(response7.status_code, 200)
#     offer1.status = "PAYMENT_MADE"
#     offer1.save()
#
#     response8 = self.client.get('/paymentCode/?offer={}'.format(offer1.id),
#                                 HTTP_AUTHORIZATION='Token ' + token2.key)
#     self.assertEqual(response8.status_code, 200)
#
#     offer1.status = "CONTRACT_MADE"
#     offer1.save()
#     data5 = {"paymentCode": "EEE"}
#     response9 = self.client.put('/paymentCode/', data5, format='json',
#                                 HTTP_AUTHORIZATION='Token ' + token.key)
#
#     print(Offer.objects.filter(pk=offer1.id).first().status)
#     #self.assertEqual(response9.status_code, 200)
#
#     print("\n\nPASSED\n\n")
#
# def test_create_offer_customer(self):
#     print("TEST_CREATE_OFFER_CUSTOMER\n")
#
#     # Populate database
#     print("Populating database...\n")
#
#     SystemConfiguration.objects.create(minimumPrice='20', currency='EUR', paypalTax='2.9', creditCardTax='1.9',
#                                        vat='21', profit='7', corporateEmail='info@grooving.com',
#                                        reportEmail='report@grooving.com', appName='Grooving',
#                                        slogan='Connecting artist with you', termsText='Terms & conditions',
#                                        privacyText='Privacy text', logo='')
#
#     user1 = User.objects.create(username='artist1', password=make_password('artist1artist1'),
#                                               first_name='Cdds', last_name='Pedro',
#                                               email='artist1@gmail.com')
#
#     user2 = User.objects.create(username='customer1', password=make_password('customer1customer1'),
#                                           first_name='Cdds', last_name='Pedro',
#                                           email='customer1@gmail.com')
#
#     date = datetime.datetime(2020, 2, 7, 8, 49, 56, 81433, pytz.UTC)
#
#     customer1 = Customer.objects.create(holder="customer1", expirationDate=date, user=user2,
#                                         number=9393393939393)
#
#     zone1 = Zone.objects.create(name="Sevilla Sur")
#     zone1.save()
#
#     event_location = EventLocation.objects.create(name="Sala Rajoy", address="C/Madrid",
#                                                    equipment="Speakers and microphone",
#                                                    description="The best event location",
#                                                    zone=zone1, customer_id=customer1.id)
#
#     portfolio1 = Portfolio.objects.create(artisticName="Juanartist")
#     portfolio1.zone.add(zone1)
#     portfolio1.save()
#
#     artist1 = Artist.objects.create(user=user1, portfolio=portfolio1, phone='600304999')
#
#     performance = Performance.objects.create(info="info", hours=3, price=200.0)
#     payment_package1 = PaymentPackage.objects.create(description="Paymentcription",
#                                                      portfolio=portfolio1, performance=performance)
#
#     fare= Fare.objects.create(priceHour=20.0)
#     payment_package2 = PaymentPackage.objects.create(description="Paymentcription",
#                                                      portfolio=portfolio1, fare=fare)
#
#     custom = Custom.objects.create(minimumPrice=50.0)
#     payment_package3 = PaymentPackage.objects.create(description="Paymentcription",
#                                                      portfolio=portfolio1, custom=custom)
#
#     # Start test
#     print("Launching test...\n")
#
#     loginBody = {"username": "customer1", "password": "customer1customer1"}
#     response = self.client.post("/api/login/", loginBody, format='json')
#     self.assertEqual(response.status_code, 200)
#
#     token_num = response.get('x-auth')
#     token = Token.objects.all().filter(pk=token_num).first()
#     print("--Token generated: " + token.key)
#
#     performanceOfferBody = {
#         "description": "This is a description",
#         "date": "2019-05-10T10:00:00",
#         "paymentPackage_id": payment_package1.id,
#         "eventLocation_id": event_location.id,
#         "transaction": {
#             "holder": "Sebastian Lopez",
#             "number": "4831288402940405",
#             "expirationDate": "1221",
#             "cvv": "772"
#         }
#     }
#
#     performanceOfferResponse = self.client.post('/offer/', performanceOfferBody, format='json',
#                                 HTTP_AUTHORIZATION='Token '+token.key)
#     self.assertEqual(performanceOfferResponse.status_code, 201)
#     print("--Performance offer:\n" + str(performanceOfferResponse.content))
#
#     fareOfferBody = {
#         "description": "This is a description",
#         "date": "2019-05-10T10:00:00",
#         "hours": 2.5,
#         "paymentPackage_id": payment_package2.id,
#         "eventLocation_id": event_location.id,
#         "transaction": {
#             "paypalCustomer": "customer1@paypal.com"
#         }
#     }
#
#     fareOfferResponse = self.client.post('/offer/', fareOfferBody, format='json',
#                                                 HTTP_AUTHORIZATION='Token ' + token.key)
#     self.assertEqual(fareOfferResponse.status_code, 201)
#     print("--Fare offer:\n" + str(fareOfferResponse.content))
#
#     customOfferBody = {
#         "description": "This is a description",
#         "date": "2019-05-10T10:00:00",
#         "hours": 2.5,
#         "price": 100.0,
#         "paymentPackage_id": payment_package3.id,
#         "eventLocation_id": event_location.id,
#         "transaction": {
#             "holder": "Sebastian Lopez",
#             "number": "4831288402940405",
#             "expirationDate": "1221",
#             "cvv": "772"
#         }
#     }
#
#     customOfferResponse = self.client.post('/offer/', customOfferBody, format='json',
#                                          HTTP_AUTHORIZATION='Token ' + token.key)
#     #self.assertEqual(customOfferResponse.status_code, 201)
#     print("--Custom offer:\n" + str(customOfferResponse.content))
#
#     badRequestBody = {
#         "description": "This is a description",
#         "date": "2019-05-10T10:00:00",
#         "hours": 2.5,
#         "price": 10.0,
#         "paymentPackage_id": payment_package3.id,
#         "eventLocation_id": event_location.id,
#     }
#
#     badRequestResponse = self.client.post('/offer/', badRequestBody, format='json',
#                                           HTTP_AUTHORIZATION='Token ' + token.key)
#
#     self.assertEqual(badRequestResponse.status_code, 400)
#     print("--Bad request expected:\n" + str(badRequestResponse.content))
#
#     nonAuthenticatedBody = {
#         "description": "This is a description",
#         "date": "2019-05-10T10:00:00",
#         "hours": 2.5,
#         "price": 100.0,
#         "paymentPackage_id": payment_package3.id,
#         "eventLocation_id": event_location.id
#     }
#
#     nonAuthenticatedResponse = self.client.post('/offer/', nonAuthenticatedBody, format='json')
#
#     self.assertEqual(nonAuthenticatedResponse.status_code, 401)
#     print("--User non authenticated:\n" + str(nonAuthenticatedResponse.content))
#
#     print("\nPASSED\n")
