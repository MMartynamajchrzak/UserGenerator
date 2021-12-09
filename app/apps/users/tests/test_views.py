from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

CREATE_NO_PARAM = "/users/"
CREATE_TEN_USERS = "/users/10/"


class Login:
    PASSWORD = "test_pass"

    def __init__(self):
        self.client = APIClient()

    def login(self):
        data = {
            "username": "test_user",
            "password": Login.PASSWORD
        }
        # auth
        register = self.client.post("/api_users/register/", data, format="json")
        token = self.client.post("/api_users/login/", data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.data["access"]}')


class TestAuthorizedUser(TestCase):

    def test_create_one_user_with_all_fields_filled_successful(self):
        # auth user
        user = Login()
        user.login()

        payload = {
            "gender": "male",
            "first_name": "Mateusz",
            "last_name": "Perkins",
            "country": "United Kingdom",
            "city": "Opole",
            "email": "mario.perkins@example.com",
            "username": "organicgoose823",
            "phone": "0716-846-384",
        }
        # create user
        response = user.client.post(CREATE_NO_PARAM, payload)

        # all filled fields are used
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data[0]["country"], payload["country"])
        self.assertEqual(response.data[0]["email"], payload["email"])
        self.assertEqual(response.data[0]["username"], payload["username"])

    def test_create_one_user_with_no_fields_passed_all_fields_filled(self):
        # auth user
        user = Login()
        user.login()

        # create user with no data passed
        # all data should be automatically generated from external API
        response = user.client.post(CREATE_NO_PARAM)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data[0]["country"])
        self.assertIsNotNone(response.data[0]["username"])
        self.assertIsNotNone(response.data[0]["last_name"])

    def test_filled_fields_being_used_rest_from_external_api(self):
        # auth user
        user = Login()
        user.login()

        payload = {
            "first_name": "Test",
            "last_name": "Test Last",
            "city": "London"
        }

        response = user.client.post(CREATE_NO_PARAM, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data[0]["first_name"], payload["first_name"])
        self.assertEqual(response.data[0]["last_name"], payload["last_name"])
        self.assertIsNotNone(response.data[0]["country"])
        self.assertIsNotNone(response.data[0]["username"])

    def test_fields_passed_being_user_in_one_generated_users_rest_random(self):
        # auth user
        user = Login()
        user.login()

        payload = [
            {
                "first_name": "Test",
                "last_name": "Test Last",
                "city": "London"
            },
            {
                "first_name": "Test2",
                "last_name": "Test2 Last",
                "city": "Paris"
            }
        ]
        # Generate 10 users
        # Only two of them will have passed fields
        response = user.client.post(CREATE_TEN_USERS, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.data[9]["first_name"], payload[0]["first_name"])
        self.assertNotEqual(response.data[3]["last_name"], payload[0]["last_name"])
        self.assertNotEqual(response.data[4]["last_name"], payload[1]["last_name"])
        self.assertEqual(response.data[0]["city"], payload[0]["city"])
        self.assertEqual(response.data[1]["city"], payload[1]["city"])
        self.assertEqual(response.data[1]["last_name"], payload[1]["last_name"])
        self.assertEqual(len(response.data), 10)
