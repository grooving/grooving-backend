from django.test import TestCase

from Grooving.models import Offer, MoneyField, Customer, CreditCardField, Artist, Portfolio, User, Calendar,PaymentPackage,EventLocation,Zone
from datetime import datetime
from rest_framework.test import APITestCase
# Create your tests here.


class OfferTestCase(TestCase):


    def test_accept_offer(self):

        credit_card1 = CreditCardField('Pedro Rodriguez', datetime.now(), '1234567890123456', '203')
        user1 = User()
        user1.username = "pedro"
        user1.id = "42"
        user1.email = "pedro@pedro.com"
        user1.password = "pedro"
        user1.save()
        customer1 = Customer()
        customer1.photo = "https://conectandomeconlau.com.co/wp-content/uploads/2018/03/%C2%BFTienes-las-caracteri%CC%81sticas-para-ser-un-Artista.png"
        customer1.id = "41"
        customer1.phone = "959959959"
        customer1.paypalAccount = "user=paypal,password=paypal"
        customer1.creditCard = credit_card1
        customer1.iban = "DE89 3704 0044 0532 0130 00"
        customer1.user_id = "42"

        customer1.save()

        days = [True] * 366
        print(days)
        calendar1 = Calendar(year=2019, days=days)
        calendar1.id = "44"
        calendar1.save()
        user2 = User()
        user2.email = "juan@juan.com"
        user2.username = "artist"
        user2.password= "artist"
        user2.id = "43"
        user2.save()
        artist1 = Artist()
        artist1.photo = "https://conectandomeconlau.com.co/wp-content/uploads/2018/03/%C2%BFTienes-las-caracteri%CC%81sticas-para-ser-un-Artista.png"
        artist1.id ="56"
        artist1.iban = "AD1400080001001234567890"
        artist1.phone = "999999999"
        artist1.paypalAccount = "user=artistpay,password=artistpay"
        artist1.user_id = "43"

        portfolio1 = Portfolio()
        portfolio1.calendar = calendar1
        portfolio1.artisticName = "Juanartist"

        money = MoneyField('100.0', 'EUR')

        paymentPackage = PaymentPackage()
        paymentPackage.id = "87"
        paymentPackage.description = "paymentPackage description"
        paymentPackage.appliedVAT = "0.07"
        paymentPackage.save()
        zone1 = Zone()
        zone1.id = "50"
        zone1.name = "Sevilla Sur"
        zone1.save()
        eventLocation1 = EventLocation()
        eventLocation1.name = "Sala Rajoy"
        eventLocation1.address = "C/Madrid"
        eventLocation1.equipment = "Speakers and microphone"
        eventLocation1.description = "THe best event location"
        eventLocation1.customer_id = "41"
        eventLocation1.zone_id = "50"

        eventLocation1.id = "45"
        eventLocation1.save()

        offer1 = Offer(description="Offer1", status='PENDING', date=datetime.now(), hours=2, paymentCode='EEE')
        offer1.paymentPackage_id = "87"
        offer1.eventLocation_id = "45"
        offer1.id = '40'
        offer1.save()
        self.client.login(username='artist', password='artist')

        response = self.client.get('/offers/41/', format='json')
        '''self.assertEqual(response.status_code, 200)'''
        print(response)
        self.client.logout()
        print(offer1.status)
