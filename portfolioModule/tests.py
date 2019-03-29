from django.test import TestCase

from Grooving.models import Portfolio, PortfolioModule, ArtisticGender, Customer, Artist, Portfolio, User, Calendar,PaymentPackage,EventLocation,Zone
from datetime import datetime
from rest_framework.test import APITestCase
# Create your tests here.


class PortfolioTestCase(TestCase):

    def test_show_portfolio(self):

        user1 = User()
        user1.username = "pedro"
        user1.id = "42"
        user1.email = "pedro@pedro.com"
        user1.password = "pedro"
        user1.save()

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

        artisticGender1 = ArtisticGender()
        artisticGender1.name = "Rock"
        artisticGender1.save()

        artisticGender2 = ArtisticGender()
        artisticGender2.name = "Blues"
        artisticGender2.parentGender = id
        artisticGender2.save()

        portfolio1 = Portfolio()
        portfolio1.id = "24"
        portfolio1.artisticName = "Juanartist"
        portfolio1.save()

        portfolioModule1 = PortfolioModule()
        portfolioModule1.type = "PHOTO"
        portfolioModule1.link = "https://conectandomeconlau.com.co/wp-content/uploads/2018/03/%C2%BFTienes-las-caracteri%CC%81sticas-para-ser-un-Artista.png"
        portfolioModule1.description = "Modulo Photo"
        portfolioModule1.portfolio = "24"
        portfolioModule1.save()

        portfolioModule2 = PortfolioModule()
        portfolioModule2.type = 'VIDEO'
        portfolioModule2.link = "https://conectandomeconlau.com.co/wp-content/uploads/2018/03/%C2%BFTienes-las-caracteri%CC%81sticas-para-ser-un-Artista.png"
        portfolioModule2.description = "Modulo Video"
        portfolioModule2.portfolio = "24"
        portfolioModule2.save()


        paymentPackage = PaymentPackage()
        paymentPackage.id = "87"
        paymentPackage.description = "paymentPackage description"
        paymentPackage.appliedVAT = "0.07"
        paymentPackage.portfolio = "24"
        paymentPackage.save()

        zone1 = Zone()
        zone1.id = "50"
        zone1.name = "Sevilla Sur"
        zone1.save()

        artist1.portfolio = "24"
        artist1.save()

        self.client.login(username='artist', password='artist')
        response = self.client.get('/portfolio/24', format='json')
        '''self.assertEqual(response.status_code, 200)'''
        print(response)

