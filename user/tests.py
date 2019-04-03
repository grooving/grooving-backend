
from rest_framework.test import APITestCase
from user.views import ArtistRegister,CustomerRegister

class UserTestCase(APITestCase):

    def test_signup_artist(self):

        data1={"first_name": "deffefeeffefe", "last_name": "david1", "password": "perroperro",
                "confirm_password": "perroperro", "username": "customer100", "email": "kiqo@gmail.com"}

        response = self.client.post("/signupArtist/",data1,format='json')
        self.assertEqual(response.status_code, 201)


    def test_signup_customer(self):

        data1={"first_name": "deffefeeffefe", "last_name": "david1", "password": "perroperro",
              "confirm_password": "perroperro", "username": "customer101", "email": "kiqo@gmail.com"}

        response = self.client.post("/signupCustomer/",data1,format='json')
        self.assertEqual(response.status_code, 201)