from django.test import TestCase

from Grooving.models import Portfolio, Customer, Artist, Portfolio, User, Zone, EventLocation
from datetime import datetime
from rest_framework.test import APITestCase
# Create your tests here.

class ShowCustomerInformation(TestCase):

    def test_show_personal_information_customer(self):
        user1 = User()
        user1.username = "LuzMaria"
        user1.id = "1"
        user1.email = "luz@maria.com"
        user1.password = "LuzMaría"
        user1.save()

        zone1 = Zone()
        zone1.name = "Madrid"
        zone1.parentZone = None
        zone1.save()

        customer1 = Customer()
        customer1.photo = "https://conectandomeconlau.com.co/wp-content/uploads/2018/03/%C2%BFTienes-las-caracteri%CC%81sticas-para-ser-un-Artista.png"
        customer1.id = "1"
        customer1.iban = "AD1400080001001234567890"
        customer1.phone = "622334447"
        customer1.paypalAccount = "user=payme,password=please"
        customer1.user_id = "1"
        customer1.holder = "Luz"
        customer1.expirationDate = datetime.now()
        customer1.cvv = 888
        customer1.save()

        eventLocation1 = EventLocation()
        eventLocation1.name = "Bar Pepe"
        eventLocation1.address = "Address"
        eventLocation1.equipment = "None"
        eventLocation1.description = "Small place but very famous"
        eventLocation1.zone = zone1
        eventLocation1.customer = customer1
        eventLocation1.save()

        eventLocation2 = EventLocation()
        eventLocation2.name = "Bar Joselito"
        eventLocation2.address = "Address2"
        eventLocation2.equipment = "Nothing"
        eventLocation2.description = "Small place but incredibly nice"
        eventLocation2.zone = zone1


        self.client.force_login(user1)
        response = self.client.get('/customer/personalInformation/', format='json')
        self.assertEqual(response.status_code, 200)
        result = response.json()
        print(len(result))
        item_dict = response.json()
        print(item_dict)
        #We check that only one user is retrieved
        self.assertTrue(len(item_dict) == 6)
        print(response)
        self.client.logout()

    def test_show_personal_information_artist_forbidden(self):

        user1 = User()
        user1.username = "LuzMaria"
        user1.id = "1"
        user1.email = "luz@maria.com"
        user1.password = "LuzMaría"
        user1.save()

        portfolio = Portfolio()
        portfolio.id = "1"
        portfolio.artisticName = "María de la Luz"
        portfolio.save()

        artist1 = Artist()
        artist1.photo = "https://conectandomeconlau.com.co/wp-content/uploads/2018/03/%C2%BFTienes-las-caracteri%CC%81sticas-para-ser-un-Artista.png"
        artist1.id = "1"
        artist1.iban = "AD1400080001001234567890"
        artist1.phone = "622334447"
        artist1.paypalAccount = "user=payme,password=please"
        artist1.user_id = "1"
        artist1.portfolio = portfolio
        artist1.save()

        self.client.force_login(user1)
        response = self.client.get('/customer/personalInformation/', format='json')
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_show_personal_information_admin_forbidden(self):

        user1 = User()
        user1.username = "LuzMaria"
        user1.id = "1"
        user1.email = "luz@maria.com"
        user1.password = "LuzMaría"
        user1.is_staff = True
        user1.save()

        self.client.force_login(user1)
        response = self.client.get('/customer/personalInformation/', format='json')
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_show_personal_information_anonymous_forbidden(self):

        response = self.client.get('/customer/personalInformation/', format='json')
        self.assertEqual(response.status_code, 403)
