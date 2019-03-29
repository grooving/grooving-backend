from django.test import TestCase
from rest_framework.authtoken.models import Token
from Grooving.models import Portfolio, ArtisticGender, Customer, Artist, Portfolio, User, Calendar,PaymentPackage,EventLocation,Zone
from datetime import datetime
from django.contrib.auth.hashers import make_password


class ShowArtistInformation(TestCase):

    def test_show_personal_information_artist(self):

        user1_artist1 = User.objects.create(username='artist1', password=make_password('artist1'),
                                            first_name='Bunny', last_name='Fufuu',
                                            email='artist1@gmail.com')
        user1_artist1.save()

        zone1 = Zone.objects.create(name="Sevilla Sur")
        zone1.save()

        portfolio1 = Portfolio.objects.create(artisticName="Juanartist")
        portfolio1.zone.add(zone1)
        portfolio1.save()

        artist1 = Artist.objects.create(user=user1_artist1, portfolio=portfolio1, phone='600304999')
        artist1.save()

        data1 = {"username": "artist1", "password": "artist1"}
        response = self.client.post("/api/login/", data1, format='json')

        token_num = response.get('x-auth')
        token = Token.objects.all().filter(pk=token_num).first()

        self.assertEqual(response.status_code, 200)

        response2 = self.client.get('/artist/personalInformation/', format='json', HTTP_AUTHORIZATION='Token ' + token.key)
        self.assertEqual(response2.status_code, 200)
        result = response2.json()
        item_dict = response2.json()
        self.assertTrue(len(item_dict) == 6)

        self.client.logout()

    def test_show_personal_information_customer_forbidden(self):

        user1_customer = User.objects.create(username='customer1', password=make_password('customer1'),
                                             first_name='Bunny', last_name='Fufuu',
                                             email='customer1@gmail.com')
        user1_customer.save()

        zone1 = Zone.objects.create(name="Sevilla Sur")
        zone1.save()

        customer1 = Customer.objects.create(user=user1_customer, holder="Juan", number='600304999', cvv=999,
                                            expirationDate=datetime.now())
        customer1.save()

        event_location1 = EventLocation.objects.create(name="Sala Rajoy", address="C/Madrid",
                                                       equipment="Speakers and microphone",
                                                       description="The best event location", zone=zone1,
                                                       customer=customer1)
        event_location1.save()

        data1 = {"username": "customer1", "password": "customer1"}
        response = self.client.post("/api/login/", data1, format='json')

        token_num = response.get('x-auth')
        token = Token.objects.all().filter(pk=token_num).first()

        self.assertEqual(response.status_code, 200)

        response2 = self.client.get('/artist/personalInformation/', format='json',
                                    HTTP_AUTHORIZATION='Token ' + token.key)
        self.assertEqual(response2.status_code, 403)
        self.client.logout()

    def test_show_personal_information_admin_forbidden(self):

        user1_artist1 = User.objects.create(username='artist1', password=make_password('artist1'),
                                            first_name='Bunny', last_name='Fufuu',
                                            email='artist1@gmail.com', is_staff=True)
        user1_artist1.save()

        self.client.force_login(user1_artist1)

        response2 = self.client.get('/artist/personalInformation/', format='json')
        self.assertEqual(response2.status_code, 403)
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

        self.assertTrue(len(item_dict['results']) == 2)
