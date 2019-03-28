from django.test import TestCase

from Grooving.models import Portfolio, ArtisticGender, Customer, Artist, Portfolio, User, Calendar,PaymentPackage,EventLocation,Zone
from datetime import datetime


class ShowArtistInformation(TestCase):

    def test_show_personal_information_artist(self):

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
        response = self.client.get('/artist/personalInformation/', format='json')
        self.assertEqual(response.status_code, 200)
        result = response.json()
        item_dict = response.json()
        self.assertTrue(len(item_dict) == 6)
        print(response)
        self.client.logout()

    def test_show_personal_information_customer_forbidden(self):

        user1 = User()
        user1.username = "LuzMaria"
        user1.id = "1"
        user1.email = "luz@maria.com"
        user1.password = "LuzMaría"
        user1.save()

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

        self.client.force_login(user1)
        response = self.client.get('/artist/personalInformation/', format='json')
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
        response = self.client.get('/artist/personalInformation/', format='json')
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_show_personal_information_anonymous_forbidden(self):

        response = self.client.get('/artist/personalInformation/', format='json')
        self.assertEqual(response.status_code, 403)


class ListArtistTestCase(TestCase):

    def test_list_artists(self):

        user = User()
        user.email = "juan@juan.com"
        user.username = "artist"
        user.password = "artist"
        user.id = "43"
        user.save()

        portfolio1 = Portfolio()
        portfolio1.id = "2"
        portfolio1.artisticName = "Jose"
        portfolio1.save()

        paymentPackage = PaymentPackage()
        paymentPackage.id = "87"
        paymentPackage.description = "paymentPackage description"
        paymentPackage.appliedVAT = "0.07"
        paymentPackage.portfolio = portfolio1
        paymentPackage.save()

        artista = Artist()
        artista.photo = "https://conectandomeconlau.com.co/wp-content/uploads/2018/03/%C2%BFTienes-las-caracteri%CC%81sticas-para-ser-un-Artista.png"
        artista.id = "56"
        artista.iban = "AD1400080001001234567890"
        artista.phone = "999999999"
        artista.paypalAccount = "user=artist,password=artist"
        artista.user_id = "43"
        artista.portfolio = portfolio1
        artista.save()

        response = self.client.get('/artists/'.format(1), format='json')
        self.assertEqual(response.status_code, 200)
        item_dict = response.json()
        self.assertTrue(len(item_dict['results']) == 1)
        print(response)

    def test_list_artists_filter_artistic_name(self):

        user = User()
        user.email = "juan@juan.com"
        user.username = "artist"
        user.password = "artist"
        user.id = "43"
        user.save()

        portfolio1 = Portfolio()
        portfolio1.id = "2"
        portfolio1.artisticName = "Jose"
        portfolio1.save()

        paymentPackage = PaymentPackage()
        paymentPackage.id = "87"
        paymentPackage.description = "paymentPackage description"
        paymentPackage.appliedVAT = "0.07"
        paymentPackage.portfolio = portfolio1
        paymentPackage.save()

        artista = Artist()
        artista.photo = "https://conectandomeconlau.com.co/wp-content/uploads/2018/03/%C2%BFTienes-las-caracteri%CC%81sticas-para-ser-un-Artista.png"
        artista.id = "56"
        artista.iban = "AD1400080001001234567890"
        artista.phone = "999999999"
        artista.paypalAccount = "user=artist,password=artist"
        artista.user_id = "43"
        artista.portfolio = portfolio1
        artista.save()

        user2 = User()
        user2.email = "juanjo@juanjo.com"
        user2.username = "artist2"
        user2.password = "artist2"
        user2.id = "44"
        user2.save()

        portfolio2 = Portfolio()
        portfolio2.id = "3"
        portfolio2.artisticName = "María se fue a la cama a las diez"
        portfolio2.save()

        paymentPackage2 = PaymentPackage()
        paymentPackage2.id = "88"
        paymentPackage2.description = "paymentPackage description 2222222222"
        paymentPackage2.appliedVAT = "0.07"
        paymentPackage2.portfolio = portfolio2
        paymentPackage2.save()

        artista2 = Artist()
        artista2.photo = "https://conectandomeconlau.com.co/wp-content/uploads/2018/03/%C2%BFTienes-las-caracteri%CC%81sticas-para-ser-un-Artista.png"
        artista2.id = "57"
        artista2.iban = "AD1400080001001234567890"
        artista2.phone = "999999999"
        artista2.paypalAccount = "user=artist,password=artist"
        artista2.user_id = "44"
        artista2.portfolio = portfolio2
        artista2.save()

        response = self.client.get('/artists/?artisticName=Jose', format='json')
        item_dict = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(item_dict['results']) == 1)
        print(response)

    def test_list_artists_filter_artistic_gender(self):
        user = User()
        user.email = "juan@juan.com"
        user.username = "artist"
        user.password = "artist"
        user.id = "43"
        user.save()

        artisticGender2 = ArtisticGender()
        artisticGender2.id = "1"
        artisticGender2.name = "Pop"
        artisticGender2.parentGender = None
        artisticGender2.save()

        portfolio1 = Portfolio()
        portfolio1.id = "2"
        portfolio1.artisticName = "Jose"
        portfolio1.save()
        portfolio1.artisticGender.add(artisticGender2)
        portfolio1.save()

        paymentPackage = PaymentPackage()
        paymentPackage.id = "87"
        paymentPackage.description = "paymentPackage description"
        paymentPackage.appliedVAT = "0.07"
        paymentPackage.portfolio = portfolio1
        paymentPackage.save()

        artista = Artist()
        artista.photo = "https://conectandomeconlau.com.co/wp-content/uploads/2018/03/%C2%BFTienes-las-caracteri%CC%81sticas-para-ser-un-Artista.png"
        artista.id = "56"
        artista.iban = "AD1400080001001234567890"
        artista.phone = "999999999"
        artista.paypalAccount = "user=artist,password=artist"
        artista.user_id = "43"
        artista.portfolio = portfolio1
        artista.save()

        user2 = User()
        user2.email = "juanjo@juanjo.com"
        user2.username = "artist2"
        user2.password = "artist2"
        user2.id = "44"
        user2.save()

        artisticGender = ArtisticGender()
        artisticGender.id = "2"
        artisticGender.name = "Rock"
        artisticGender.parentGender = None
        artisticGender.save()

        portfolio2 = Portfolio()
        portfolio2.id = "3"
        portfolio2.artisticName = "María se fue a la cama a las diez"
        portfolio2.save()
        portfolio2.artisticGender.add(artisticGender)
        portfolio2.save()

        paymentPackage2 = PaymentPackage()
        paymentPackage2.id = "88"
        paymentPackage2.description = "paymentPackage description 2222222222"
        paymentPackage2.appliedVAT = "0.07"
        paymentPackage2.portfolio = portfolio2
        paymentPackage2.save()

        artista2 = Artist()
        artista2.photo = "https://conectandomeconlau.com.co/wp-content/uploads/2018/03/%C2%BFTienes-las-caracteri%CC%81sticas-para-ser-un-Artista.png"
        artista2.id = "57"
        artista2.iban = "AD1400080001001234567890"
        artista2.phone = "999999999"
        artista2.paypalAccount = "user=artist,password=artist"
        artista2.user_id = "44"
        artista2.portfolio = portfolio2
        artista2.save()

        response = self.client.get('/artists/?artisticGender=Rock', format='json')
        item_dict = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(item_dict['results']) == 1)
        print(response)

    def test_list_artists_filter_artistic_gender_no_matches(self):
        user = User()
        user.email = "juan@juan.com"
        user.username = "artist"
        user.password = "artist"
        user.id = "43"
        user.save()

        artisticGender2 = ArtisticGender()
        artisticGender2.id = "1"
        artisticGender2.name = "Pop"
        artisticGender2.parentGender = None
        artisticGender2.save()

        portfolio1 = Portfolio()
        portfolio1.id = "2"
        portfolio1.artisticName = "Jose"
        portfolio1.save()

        portfolio1.artisticGender.add(artisticGender2)
        portfolio1.save()

        paymentPackage = PaymentPackage()
        paymentPackage.id = "87"
        paymentPackage.description = "paymentPackage description"
        paymentPackage.appliedVAT = "0.07"
        paymentPackage.portfolio = portfolio1
        paymentPackage.save()

        artista = Artist()
        artista.photo = "https://conectandomeconlau.com.co/wp-content/uploads/2018/03/%C2%BFTienes-las-caracteri%CC%81sticas-para-ser-un-Artista.png"
        artista.id = "56"
        artista.iban = "AD1400080001001234567890"
        artista.phone = "999999999"
        artista.paypalAccount = "user=artist,password=artist"
        artista.user_id = "43"
        artista.portfolio = portfolio1
        artista.save()

        user2 = User()
        user2.email = "juanjo@juanjo.com"
        user2.username = "artist2"
        user2.password = "artist2"
        user2.id = "44"
        user2.save()

        artisticGender = ArtisticGender()
        artisticGender.id = "2"
        artisticGender.name = "Rock"
        artisticGender.parentGender = None
        artisticGender.save()

        portfolio2 = Portfolio()
        portfolio2.id = "3"
        portfolio2.artisticName = "María se fue a la cama a las diez"
        portfolio2.save()
        portfolio2.artisticGender.add(artisticGender)
        portfolio2.save()

        paymentPackage2 = PaymentPackage()
        paymentPackage2.id = "88"
        paymentPackage2.description = "paymentPackage description 2222222222"
        paymentPackage2.appliedVAT = "0.07"
        paymentPackage2.portfolio = portfolio2
        paymentPackage2.save()

        artista2 = Artist()
        artista2.photo = "https://conectandomeconlau.com.co/wp-content/uploads/2018/03/%C2%BFTienes-las-caracteri%CC%81sticas-para-ser-un-Artista.png"
        artista2.id = "57"
        artista2.iban = "AD1400080001001234567890"
        artista2.phone = "999999999"
        artista2.paypalAccount = "user=artist,password=artist"
        artista2.user_id = "44"
        artista2.portfolio = portfolio2
        artista2.save()

        response = self.client.get('/artists/?artisticGender=Country', format='json')
        item_dict = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(item_dict['results']) == 0)
        print(response)

    def test_list_artists_filter_artistic_gender_parent_match(self):
        user = User()
        user.email = "juan@juan.com"
        user.username = "artist"
        user.password = "artist"
        user.id = "43"
        user.save()

        artisticGender2 = ArtisticGender()
        artisticGender2.id = "1"
        artisticGender2.name = "Musica"
        artisticGender2.parentGender = None
        artisticGender2.save()

        portfolio1 = Portfolio()
        portfolio1.id = "2"
        portfolio1.artisticName = "Jose"
        portfolio1.save()
        portfolio1.artisticGender.add(artisticGender2)
        portfolio1.save()

        paymentPackage = PaymentPackage()
        paymentPackage.id = "87"
        paymentPackage.description = "paymentPackage description"
        paymentPackage.appliedVAT = "0.07"
        paymentPackage.portfolio = portfolio1
        paymentPackage.save()

        artista = Artist()
        artista.photo = "https://conectandomeconlau.com.co/wp-content/uploads/2018/03/%C2%BFTienes-las-caracteri%CC%81sticas-para-ser-un-Artista.png"
        artista.id = "56"
        artista.iban = "AD1400080001001234567890"
        artista.phone = "999999999"
        artista.paypalAccount = "user=artist,password=artist"
        artista.user_id = "43"
        artista.portfolio = portfolio1
        artista.save()

        user2 = User()
        user2.email = "juanjo@juanjo.com"
        user2.username = "artist2"
        user2.password = "artist2"
        user2.id = "44"
        user2.save()

        artisticGender = ArtisticGender()
        artisticGender.id = "2"
        artisticGender.name = "Rock"
        artisticGender.parentGender = artisticGender2
        artisticGender.save()

        artisticGender3 = ArtisticGender()
        artisticGender3.id = "3"
        artisticGender3.name = "Punk"
        artisticGender3.parentGender = artisticGender
        artisticGender3.save()

        portfolio2 = Portfolio()
        portfolio2.id = "3"
        portfolio2.artisticName = "María se fue a la cama a las diez"
        portfolio2.save()
        portfolio2.artisticGender.add(artisticGender3)
        portfolio2.save()

        paymentPackage2 = PaymentPackage()
        paymentPackage2.id = "88"
        paymentPackage2.description = "paymentPackage description 2222222222"
        paymentPackage2.appliedVAT = "0.07"
        paymentPackage2.portfolio = portfolio2
        paymentPackage2.save()

        artista2 = Artist()
        artista2.photo = "https://conectandomeconlau.com.co/wp-content/uploads/2018/03/%C2%BFTienes-las-caracteri%CC%81sticas-para-ser-un-Artista.png"
        artista2.id = "57"
        artista2.iban = "AD1400080001001234567890"
        artista2.phone = "999999999"
        artista2.paypalAccount = "user=artist,password=artist"
        artista2.user_id = "44"
        artista2.portfolio = portfolio2
        artista2.save()

        response = self.client.get('/artists/?artisticGender=Musica', format='json')
        item_dict = response.json()
        self.assertEqual(response.status_code, 200)
        print(item_dict)
        self.assertTrue(len(item_dict['results']) == 2)
        print(response)
