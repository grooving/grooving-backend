from django.test import TestCase
from Grooving.models import Zone, User, Artist, Rating, EventLocation, Customer, Offer, Portfolio, PaymentPackage, Calendar, Performance
from datetime import datetime
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.contrib.auth.hashers import make_password


class RatingTestCase(TestCase):

    '''
    def test_create_rating(self):
        user1_customer = User.objects.create(username='customer1', password=make_password('customer1'),
                                             first_name='Bunny', last_name='Fufuu',
                                             email='customer1@gmail.com')
        user1_customer.save()

        zone1 = Zone.objects.create(name="Sevilla Sur")
        zone1.save()

        customer1 = Customer.objects.create(user=user1_customer, holder="Juan", number='600304999',
                                            expirationDate=datetime.now())
        customer1.save()

        event_location1 = EventLocation.objects.create(name="Sala Rajoy", address="C/Madrid",
                                                       equipment="Speakers and microphone",
                                                       description="The best event location", zone=zone1,
                                                       customer=customer1)
        event_location1.save()

        days = ['2019-06-02', '2019-08-02']

        user2_artist1 = User.objects.create(username='artist1', password=make_password('artist1'),
                                            first_name='Bunny', last_name='Fufuu',
                                            email='artist1@gmail.com')
        user2_artist1.save()

        zone1 = Zone.objects.create(name="Sevilla Sur")
        zone1.save()

        portfolio1 = Portfolio.objects.create(artisticName="Juanartist")
        portfolio1.zone.add(zone1)
        portfolio1.save()

        artist1 = Artist.objects.create(user=user2_artist1, portfolio=portfolio1, phone='600304999')
        artist1.save()

        calendar1 = Calendar.objects.create(days=days, portfolio=portfolio1)
        calendar1.save()

        performance1 = Performance.objects.create(info="info", hours=3, price=200.0)
        performance1.save()
        payment_package1 = PaymentPackage.objects.create(description="Paymentcription",
                                                         portfolio=portfolio1, performance=performance1)

        payment_package1.save()

        date = timezone.now()

        offer1 = Offer.objects.create(description="DESCRIPTIONOFFER1", status='PAYMENT_MADE', date=date, price="200",
                                      currency="EUR", hours=2, appliedVAT="0.35",
                                      paymentCode='EEE', eventLocation=event_location1, paymentPackage=payment_package1)
        offer1.save()

        data1 = {"username": "customer1", "password": "customer1"}
        response = self.client.post("/api/login/", data1, format='json')

        token_num = response.get('x-auth')
        token = Token.objects.all().filter(pk=token_num).first()

        self.assertEqual(response.status_code, 200)

        rating = Rating(score='5', comment='I love it!')
        rating.save()

        offer1.rating = rating
        offer1.save()

        response2 = self.client.get('/customer/rating/'+str(offer1.id)+'/', format='json', HTTP_AUTHORIZATION='Token ' + token.key)
        self.assertEqual(response2.status_code, 200)
        item_dict = response2.json()'''