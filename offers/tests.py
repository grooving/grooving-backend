from django.test import TestCase

from Grooving.models import Offer, Customer, Artist, Portfolio, User, Calendar,PaymentPackage,EventLocation,Zone
from datetime import datetime
from rest_framework.test import APITestCase
# Create your tests here.


class OfferTestCase(TestCase):

    def test_list_artist_offers(self):

        user1 = User()
        user1.username = "Armando"
        user1.id = "15"
        user1.email = "fire@fire.com"
        user1.password = "Armando"
        user1.save()

        customer1 = Customer()
        customer1.photo = "https://conectandomeconlau.com.co/wp-content/uploads/2018/03/%C2%BFTienes-las-caracteri%CC%81sticas-para-ser-un-Artista.png"
        customer1.id = "32"
        customer1.phone = "957689091"
        customer1.paypalAccount = "user=pay,password=you"
        customer1.iban = "DE00 3645 1143 4432 2135 01"
        customer1.user = user1
        customer1.holder = 'Pedro Rodriguez'
        customer1.expirationDate = datetime.now()
        customer1.number = '1234567890123456'
        customer1.cvv = '203'
        customer1.save()

        days = [True] * 366
        calendar1 = Calendar(year=2019, days=days)
        calendar1.id = "44"


        user2 = User()
        user2.email = "pepe@pepe.com"
        user2.username = "user2"
        user2.password = "user2"
        user2.id = "16"
        user2.save()


        portfolio1 = Portfolio()
        portfolio1.calendar = calendar1
        portfolio1.artisticName = "No me pises"
        portfolio1.id = "4"
        portfolio1.save()

        calendar1.portfolio = portfolio1
        calendar1.save()

        artist1 = Artist()
        artist1.photo = "https://conectandomeconlau.com.co/wp-content/uploads/2018/03/%C2%BFTienes-las-caracteri%CC%81sticas-para-ser-un-Artista.png"
        artist1.id = "56"
        artist1.iban = "AD1400080001011111111"
        artist1.phone = "999995555"
        artist1.paypalAccount = "user=artistpay,password=artistpay"
        artist1.user = user2
        artist1.portfolio = portfolio1
        artist1.save()

        paymentPackage = PaymentPackage()
        paymentPackage.id = "87"
        paymentPackage.description = "paymentPackage description"
        paymentPackage.appliedVAT = "0.07"
        paymentPackage.portfolio = portfolio1
        paymentPackage.save()
        zone1 = Zone()
        zone1.id = "50"
        zone1.name = "Sevilla Este"
        zone1.save()

        eventLocation1 = EventLocation()
        eventLocation1.name = "Sala Rajoy"
        eventLocation1.address = "C/Madrid"
        eventLocation1.equipment = "Speakers and microphone"
        eventLocation1.description = "THe best event location"
        eventLocation1.customer = customer1
        eventLocation1.zone = zone1
        eventLocation1.save()

        eventLocation1.id = "45"
        eventLocation1.save()

        offer1 = Offer()
        offer1.description = "Offer1"
        offer1.status = 'PENDING'
        offer1.date = datetime.now()
        offer1.hours = 2
        offer1.price = 3.4
        offer1.paymentCode = 'Code'
        offer1.paymentPackage = paymentPackage
        offer1.eventLocation = eventLocation1
        offer1.id = '40'
        offer1.save()

        #Second batch of data for the test

        user3 = User()
        user3.username = "Manuel"
        user3.id = "17"
        user3.email = "fire@fire.com"
        user3.password = "Manuel"
        user3.save()

        customer2 = Customer()
        customer2.photo = "https://conectandomeconlau.com.co/wp-content/uploads/2018/03/%C2%BFTienes-las-caracteri%CC%81sticas-para-ser-un-Artista.png"
        customer2.id = "35"
        customer2.phone = "957689091"
        customer2.paypalAccount = "user=pay,password=you"
        customer2.iban = "DE00 3645 1143 4432 2135 01"
        customer2.user = user3
        customer2.holder = 'Pedro Rodriguez'
        customer2.expirationDate = datetime.now()
        customer2.number = '1234567890123456'
        customer2.cvv = '203'
        customer2.save()

        user4 = User()
        user4.email = "pepe@pepe.com"
        user4.username = "user4"
        user4.password = "user4"
        user4.id = "20"
        user4.save()

        portfolio2 = Portfolio()
        portfolio2.calendar = calendar1
        portfolio2.artisticName = "Married to college"
        portfolio2.save()

        calendar2 = Calendar(year=2019, days=days)
        calendar2.id = "45"
        calendar2.portfolio = portfolio2
        calendar2.save()

        artist2 = Artist()
        artist2.photo = "https://conectandomeconlau.com.co/wp-content/uploads/2018/03/%C2%BFTienes-las-caracteri%CC%81sticas-para-ser-un-Artista.png"
        artist2.id = "57"
        artist2.iban = "AD1400080001011111111"
        artist2.phone = "999995555"
        artist2.paypalAccount = "user=artistpay,password=artistpay"
        artist2.user = user4
        artist2.portfolio = portfolio2
        artist2.save()

        paymentPackage2 = PaymentPackage()
        paymentPackage2.id = "88"
        paymentPackage2.description = "paymentPackage description"
        paymentPackage2.appliedVAT = "0.07"
        paymentPackage2.portfolio = portfolio2
        paymentPackage2.save()
        zone2 = Zone()
        zone2.id = "51"
        zone2.name = "Sevilla Norte"
        zone2.save()

        eventLocation2 = EventLocation()
        eventLocation2.name = "Sala Rajoy"
        eventLocation2.address = "C/Madrid"
        eventLocation2.equipment = "Speakers and microphone"
        eventLocation2.description = "THe best event location"
        eventLocation2.customer = customer2
        eventLocation2.zone = zone2

        eventLocation2.id = "46"
        eventLocation2.save()

        offer2 = Offer()
        offer2.description = "Offer2"
        offer2.status = 'PENDING'
        offer2.date = datetime.now()
        offer2.hours = 4
        offer2.paymentCode = 'Code2'
        offer2.paymentPackage = paymentPackage2
        offer2.eventLocation = eventLocation2
        offer2.id = '41'
        offer2.price = 4.4
        offer2.save()

        self.client.force_login(user2)
        response = self.client.get('/offers/', format='json')
        self.assertEqual(response.status_code, 200)
        result = response.json()
        item_dict = response.json()
        print(item_dict)
        print(len(item_dict['results']))
        self.assertTrue(len(item_dict['results']) == 1)
        print(response)
        self.client.logout()

    def test_list_customer_offers(self):

        user1 = User()
        user1.username = "Armando"
        user1.id = "15"
        user1.email = "fire@fire.com"
        user1.password = "Armando"
        user1.save()

        customer1 = Customer()
        customer1.photo = "https://conectandomeconlau.com.co/wp-content/uploads/2018/03/%C2%BFTienes-las-caracteri%CC%81sticas-para-ser-un-Artista.png"
        customer1.id = "32"
        customer1.phone = "957689091"
        customer1.paypalAccount = "user=pay,password=you"
        customer1.iban = "DE00 3645 1143 4432 2135 01"
        customer1.user = user1
        customer1.holder = 'Pedro Rodriguez'
        customer1.expirationDate = datetime.now()
        customer1.number = '1234567890123456'
        customer1.cvv = '203'
        customer1.save()

        user2 = User()
        user2.email = "pepe@pepe.com"
        user2.username = "user2"
        user2.password = "user2"
        user2.id = "16"
        user2.save()

        portfolio1 = Portfolio()
        portfolio1.artisticName = "No me pises"
        portfolio1.id = "4"
        portfolio1.save()

        days = [True] * 366
        calendar1 = Calendar(year=2019, days=days)
        calendar1.id = "44"
        calendar1.portfolio = portfolio1
        calendar1.save()

        artist1 = Artist()
        artist1.photo = "https://conectandomeconlau.com.co/wp-content/uploads/2018/03/%C2%BFTienes-las-caracteri%CC%81sticas-para-ser-un-Artista.png"
        artist1.id = "56"
        artist1.iban = "AD1400080001011111111"
        artist1.phone = "999995555"
        artist1.paypalAccount = "user=artistpay,password=artistpay"
        artist1.user = user2
        artist1.portfolio = portfolio1
        artist1.save()

        paymentPackage = PaymentPackage()
        paymentPackage.id = "87"
        paymentPackage.description = "paymentPackage description"
        paymentPackage.appliedVAT = "0.07"
        paymentPackage.portfolio = portfolio1
        paymentPackage.save()
        zone1 = Zone()
        zone1.id = "50"
        zone1.name = "Sevilla Este"
        zone1.save()

        eventLocation1 = EventLocation()
        eventLocation1.name = "Sala Rajoy"
        eventLocation1.address = "C/Madrid"
        eventLocation1.equipment = "Speakers and microphone"
        eventLocation1.description = "THe best event location"
        eventLocation1.zone = zone1
        eventLocation1.customer = customer1
        eventLocation1.save()

        eventLocation1.id = "45"
        eventLocation1.save()

        customer1.eventLocation = eventLocation1
        customer1.save()

        offer1 = Offer()
        offer1.description = "Offer1"
        offer1.status = 'PENDING'
        offer1.date = datetime.now()
        offer1.hours = 2
        offer1.price = 3.4
        offer1.paymentCode = 'Code'
        offer1.paymentPackage = paymentPackage
        offer1.eventLocation = eventLocation1
        offer1.id = '40'
        offer1.save()

        #Second batch of data for the test

        user3 = User()
        user3.username = "Manuel"
        user3.id = "17"
        user3.email = "fire@fire.com"
        user3.password = "Manuel"
        user3.save()

        customer2 = Customer()
        customer2.photo = "https://conectandomeconlau.com.co/wp-content/uploads/2018/03/%C2%BFTienes-las-caracteri%CC%81sticas-para-ser-un-Artista.png"
        customer2.id = "35"
        customer2.phone = "957689091"
        customer2.paypalAccount = "user=pay,password=you"
        customer2.iban = "DE00 3645 1143 4432 2135 01"
        customer2.user = user3
        customer2.holder = 'Pedro Rodriguez'
        customer2.expirationDate = datetime.now()
        customer2.number = '1234567890123456'
        customer2.cvv = '203'
        customer2.save()

        user4 = User()
        user4.email = "pepe@pepe.com"
        user4.username = "user4"
        user4.password = "user4"
        user4.id = "20"
        user4.save()

        portfolio2 = Portfolio()
        portfolio2.calendar = calendar1
        portfolio2.artisticName = "Married to college"
        portfolio2.save()

        calendar2 = Calendar(year=2019, days=days)
        calendar2.id = "45"
        calendar2.portfolio = portfolio2
        calendar2.save()

        artist2 = Artist()
        artist2.photo = "https://conectandomeconlau.com.co/wp-content/uploads/2018/03/%C2%BFTienes-las-caracteri%CC%81sticas-para-ser-un-Artista.png"
        artist2.id = "57"
        artist2.iban = "AD1400080001011111111"
        artist2.phone = "999995555"
        artist2.paypalAccount = "user=artistpay,password=artistpay"
        artist2.user = user4
        artist2.portfolio = portfolio2
        artist2.save()

        paymentPackage2 = PaymentPackage()
        paymentPackage2.id = "88"
        paymentPackage2.description = "paymentPackage description"
        paymentPackage2.appliedVAT = "0.07"
        paymentPackage2.portfolio = portfolio2
        paymentPackage2.save()

        offer2 = Offer()
        offer2.description = "Offer2"
        offer2.status = 'PENDING'
        offer2.date = datetime.now()
        offer2.hours = 4
        offer2.paymentCode = 'Code2'
        offer2.paymentPackage = paymentPackage2
        offer2.eventLocation = eventLocation1
        offer2.id = '41'
        offer2.price = 4.4
        offer2.save()

        self.client.force_login(user1)
        response = self.client.get('/offers/', format='json')
        self.assertEqual(response.status_code, 200)
        result = response.json()
        print(len(result))
        item_dict = response.json()
        print(item_dict)
        self.assertTrue(len(item_dict['results']) == 2)
        print(response)
        self.client.logout()

    def test_list_no_offers(self):
        #admin user
        user3 = User()
        user3.username = "Manuel"
        user3.id = "17"
        user3.email = "fire@fire.com"
        user3.password = "Manuel"
        user3.is_staff = False
        user3.save()

        portfolio2 = Portfolio()
        portfolio2.artisticName = "Married to college"
        portfolio2.save()

        artist2 = Artist()
        artist2.photo = "https://conectandomeconlau.com.co/wp-content/uploads/2018/03/%C2%BFTienes-las-caracteri%CC%81sticas-para-ser-un-Artista.png"
        artist2.id = "57"
        artist2.iban = "AD1400080001011111111"
        artist2.phone = "999995555"
        artist2.paypalAccount = "user=artistpay,password=artistpay"
        artist2.user = user3
        artist2.portfolio = portfolio2
        artist2.save()

        paymentPackage2 = PaymentPackage()
        paymentPackage2.id = "88"
        paymentPackage2.description = "paymentPackage description"
        paymentPackage2.portfolio = portfolio2
        paymentPackage2.appliedVAT = "0.07"
        paymentPackage2.save()

        self.client.force_login(user3)
        response = self.client.get('/offers/', format='json')
        self.assertEqual(response.status_code, 200)

        result = response.json()
        print(len(result))
        item_dict = response.json()
        print(item_dict)
        self.assertTrue(len(item_dict['results']) == 0)
        self.client.logout()


    def test_list_anonymous(self):

        response = self.client.get('/offers/', format='json')
        self.assertEqual(response.status_code, 403)

    def test_list_admin(self):
        #admin user
        user3 = User()
        user3.username = "Manuel"
        user3.id = "17"
        user3.email = "fire@fire.com"
        user3.password = "Manuel"
        user3.is_staff = True
        user3.save()

        self.client.force_login(user3)
        response = self.client.get('/offers/', format='json')
        self.assertEqual(response.status_code, 403)
        self.client.logout()
