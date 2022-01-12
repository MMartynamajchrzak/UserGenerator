from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.users.models import User

# urls
CREATE_NO_PARAM = "/users/"
GET_ALL_USERS = "/users/all/"

def create_n_users(n):
    return f"/users/{n}/"

USER = [{
    "gender": "male",
    "first_name": "Mateusz",
    "last_name": "Perkins",
    "country": "United Kingdom",
    "city": "Opole",
    "email": "mario.perkins@example.com",
    "username": "organicgoose823",
    "phone": "0716-846-384",
}]


class TestAuthorizedUser(TestCase):
    PASSWORD = "test_pass"

    def setUp(self):
        self.client = APIClient()

        data = {
            "username": "test_user",
            "password": TestAuthorizedUser.PASSWORD
        }
        # auth
        register = self.client.post("/api_users/register/", data, format="json")
        token = self.client.post("/api_users/login/", data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.data["access"]}')

    def test_create_one_user_with_all_fields_filled_successful(self):
        # create user
        response = self.client.post(CREATE_NO_PARAM, data=USER, format="json")

        # all filled fields are used
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data[0]["country"], USER[0]["country"])
        self.assertEqual(response.data[0]["email"], USER[0]["email"])
        self.assertEqual(response.data[0]["username"], USER[0]["username"])

    def test_create_one_user_with_no_fields_passed_all_fields_filled(self):
        # create user with no data passed
        # all data should be automatically generated from external API
        response = self.client.post(CREATE_NO_PARAM)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data[0]["country"])
        self.assertIsNotNone(response.data[0]["username"])
        self.assertIsNotNone(response.data[0]["last_name"])

    def test_filled_fields_being_used_rest_from_external_api(self):

        payload = {
            "first_name": "Test",
            "last_name": "Test Last",
            "city": "London"
        }

        response = self.client.post(CREATE_NO_PARAM, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data[0]["first_name"], payload["first_name"])
        self.assertEqual(response.data[0]["last_name"], payload["last_name"])
        self.assertIsNotNone(response.data[0]["country"])
        self.assertIsNotNone(response.data[0]["username"])

    def test_fields_passed_being_user_in_one_generated_users_rest_random(self):

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
        response = self.client.post(create_n_users(10), data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.data[9]["first_name"], payload[0]["first_name"])
        self.assertNotEqual(response.data[3]["last_name"], payload[0]["last_name"])
        self.assertNotEqual(response.data[4]["last_name"], payload[1]["last_name"])
        self.assertEqual(response.data[0]["city"], payload[0]["city"])
        self.assertEqual(response.data[1]["city"], payload[1]["city"])
        self.assertEqual(response.data[1]["last_name"], payload[1]["last_name"])
        self.assertEqual(len(response.data), 10)

    def test_list_all_users(self):

        self.client.post(create_n_users(10), data=USER, format="json")

        response = self.client.get(GET_ALL_USERS)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(USER[0]["first_name"], response.data[9]["first_name"])
        self.assertEqual(USER[0]["email"], response.data[9]["email"])
        self.assertEqual(USER[0]["country"], response.data[9]["country"])
        self.assertEqual(USER[0]["phone"], response.data[9]["phone"])
        self.assertEqual(len(response.data), 10)

    def test_show_user_detail(self):

        self.client.post(CREATE_NO_PARAM, data=USER, format="json")
        created_user = User.objects.get(email=USER[0]["email"])

        # get first user detail
        response = self.client.get(f"/users/id/{created_user.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(USER[0]))
        self.assertEqual(USER[0]["email"], response.data["email"])

    def test_update_user(self):
        self.client.post(CREATE_NO_PARAM, data=USER, format="json")
        created_user = User.objects.get(email=USER[0]["email"])

        payload = {
            "gender": "male",
            "first_name": "New_name",
            "last_name": "New_surname",
            "country": "United Kingdom",
            "city": "Opole",
            "email": "new@email.test",
            "username": "organicgoose823",
            "phone": "0716-846-384"
        }

        # get first user detail
        response = self.client.put(f"/users/id/{created_user.id}/", payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(USER[0]))
        self.assertEqual(payload["email"], response.data["email"])
        self.assertEqual(payload["last_name"], response.data["last_name"])
        self.assertEqual(payload["first_name"], response.data["first_name"])
        self.assertEqual(USER[0]["phone"], response.data["phone"])
        self.assertEqual(USER[0]["country"], response.data["country"])

    def test_delete_user(self):
        self.client.post(CREATE_NO_PARAM, data=USER, format="json")
        created_user = User.objects.get(email=USER[0]["email"])

        #delete user
        response = self.client.delete(f"/users/id/{created_user.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
