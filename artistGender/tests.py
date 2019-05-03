
from django.test import TestCase
from Grooving.models import Zone, User, Admin, ArtisticGender, Artist, Rating, EventLocation, Customer, Offer, Portfolio, PaymentPackage, Calendar, Custom
from datetime import datetime
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from rest_framework.test import APITransactionTestCase

class GenderTestCase(APITransactionTestCase):
    phater= None
    son = None
    grandson = None
    def setUp(self):
        user_admin = User.objects.create(username='admin', password=make_password('admin'), is_staff=True,
                                         is_superuser=True, first_name='Sauron', last_name='The Overlord',
                                         email="admin@grooving.com")

        user_admin.save()

        admin = Admin.objects.create(user=user_admin, language='es')
        admin.save()

        parentOfAll = ArtisticGender.objects.create(name_es="Padre de todo", name_en="Father of all")
        parentOfAll.save()
        self.phater= parentOfAll.pk

        son = ArtisticGender.objects.create(name_es="El hijo", name_en="The son", parentGender_id=parentOfAll.pk)
        son.save()
        self.son = son.pk
        grandson = ArtisticGender.objects.create(name_es="EL nieto", name_en="The grandson", parentGender_id=son.pk)
        grandson.save()
        self.grandson = grandson.pk

    def test_driver_gender_management(self):

        payload = [
            ["Hijo", "Son", self.phater, self.phater, "Sonss", "Hijso", 201, 201],
            [None, "son2", self.phater, self.phater, "Sognss", "Hijhso", 401, 401],
            ["Hijo2", None, self.phater, self.phater, "Sondss", "Hdijso", 401, 401],
            [None, None, self.phater, self.phater, "Sosnss", "Hijso", 401, 401],
            [None, None, self.phater, self.phater, "Sonss", "Hijsso", 401, 401],
            ["Hijo4", "Son4", self.son, self.phater, "Soniss", "Hipjso", 201, 201],
            ["Hijo5", "Son5", self.son, self.phater, "Sonss", "", 201, 201],
            ["Hijo6", "Son6", self.son, self.phater, None, "Hijxso", 201, 400],
            ["Hijo7", "Son7", self.son, self.grandson, "Sonnss", "Hijmso", 201, 400],
            ["Hijo8", "Son8", self.grandson, self.phater, "Sodnss", "Hidjso", 400, 201],

        ]

        indice = 1
        for data in payload:
            print("---> Test " + str(indice) + " es")
            self.template_gender(data, "es")
            print("---> Test " + str(indice) + " en")
            self.template_gender(data, "en")
            indice += 1

    def template_gender(self, arg, lang):
        user = {"username": "admin", "password": "admin"}
        response = self.client.post("/api/admin/login/", user, format='json')
        token_num = response.get("x-auth")

        response_list = self.client.get("/artisticGenders/?parentId=true", HTTP_AUTHORIZATION='Token ' + token_num,
                                        HTTP_ACCEPT_LANGUAGE=lang)

        create_name_es =arg[0] if arg[0] is None else arg[0]+lang
        create_name_en = arg[1] if arg[1] is None else arg[1] + lang
        edit_name_es = arg[4] if arg[4] is None else arg[4] + lang
        edit_name_en = arg[5] if arg[5] is None else arg[5] + lang
        print(response_list.status_code)
        self.assertEqual(200, response_list.status_code)
        create_data = {"name_es": create_name_es, "name_en": create_name_en, "parentGender": arg[2]}

        response_create = self.client.post("/artisticGender/", create_data, format="json",
                                           HTTP_AUTHORIZATION='Token ' + token_num,
                                           HTTP_ACCEPT_LANGUAGE=lang)

        print(response_create.status_code)
        self.assertEqual(arg[-2], response_create.status_code)
        if response_create.status_code == 201:
            create_gender = ArtisticGender.objects.filter(name_es=arg[0]+lang).first()
            edit_data = {"id": create_gender.pk, "name_es": edit_name_es, "name_en": edit_name_en, "parentGender": arg[3]}
            response_edit = self.client.put("/artisticGender/"+str(create_gender.pk)+"/", edit_data, format="json",
                                              HTTP_AUTHORIZATION='Token ' + token_num,
                                              HTTP_ACCEPT_LANGUAGE=lang)
            print(response_edit.status_code)
            self.assertEqual(arg[-1], response_edit.status_code)
            response_delete = self.client.delete("/artisticGender/"+str(create_gender.pk)+"/",
                                                 HTTP_AUTHORIZATION='Token ' + token_num,
                                                 HTTP_ACCEPT_LANGUAGE=lang)
            print(response_delete.status_code)
            self.assertEqual(204, response_delete.status_code)



'''from Grooving.models import Offer, Artist, Portfolio, User, Calendar, PaymentPackage, Customer
from Grooving.models import EventLocation, Zone, Performance, ArtisticGender
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
import datetime
import pytz






class ArtistGenderTestCase(APITestCase):

    def test_manage_artistGender_artist(self):

        days = ['2019-06-02', '2019-08-02', '2019-10-15', '2019-11-02']
        date = datetime.datetime(2020,2,7,8,49,56,81433, pytz.UTC)

        user1_artist1 = User.objects.create(username='artist1', password=make_password('artist1artist1'),
                                            first_name='Cdds', last_name='Pedro',
                                            email='artist1@gmail.com')
        user1_artist1.save()

        zone1 = Zone.objects.create(name="Sevilla Sur")
        zone1.save()

        artisticgender = ArtisticGender.objects.create(name="Rock")
        artisticgender.save()

        portfolio1 = Portfolio.objects.create(artisticName="Juanartist")
        portfolio1.zone.add(zone1)
        portfolio1.save()

        artist1 = Artist.objects.create(user=user1_artist1, portfolio=portfolio1, phone='600304999')
        artist1.save()

        performance1 = Performance.objects.create(info="info", hours=3, price=200.0, currency="EUR")
        performance1.save()
        payment_package1 = PaymentPackage.objects.create(description="Paymentcription", appliedVAT="0.35",
                                                         portfolio=portfolio1, performance=performance1)

        payment_package1.save()

        calendar1 = Calendar.objects.create(days=days, portfolio=portfolio1)
        calendar1.save()

        data1 = {"username": "artist1", "password": "artist1artist1"}
        response = self.client.post("/api/login/", data1, format='json')

        token_num = response.get('x-auth')
        token = Token.objects.all().filter(pk=token_num).first()
        print(token.key)
        self.assertEqual(response.status_code, 200)

        data = {"id": "" + str(artisticgender.id), "name": "Blues", "portfolio_set": [str(portfolio1.id)]}

        response1 = self.client.put('/artisticGender/{}/'.format(artisticgender.id), data, format='json',
                                    HTTP_AUTHORIZATION='Token '+token.key)
        self.assertEqual(response1.status_code, 200)

        print(response1)
        print(ArtisticGender.objects.filter(pk=artisticgender.id).first())'''
