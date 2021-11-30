from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


REGISTER_URL = '/api_users/register/'
LOGIN_URL = '/api_users/login/'


class TestApiUserViewSet(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='test_user0',
            password='test'
        )

    def test_register_user_successful(self):
        payload = {
            "username": "test_user",
            "password": "test_pass"
        }
        response = self.client.post(REGISTER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn(payload['password'], response.data)

        # check for access and refresh tokens (JWT auth)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_user_with_correct_credentials_successful(self):
        payload = {
            "username": "test_user0",
            "password": "test"
        }
        response = self.client.post(LOGIN_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(payload['password'], response.data)

        # check for access and refresh tokens (JWT auth)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_user_with_wrong_credentials_failed(self):
        payload = {
            "username": "test_user0",
            "password": "wrong_password"
        }
        response = self.client.post(LOGIN_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
