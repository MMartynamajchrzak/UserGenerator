from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.api_users.serializers import ApiUserSerializer, TokenSerializer


class TestApiUserSerializer(TestCase):
    def test_api_user_fields_content(self):
        user = get_user_model().objects.create_user(
            username='test_username',
            password='test_password'
        )
        serializer = ApiUserSerializer(user)
        data = serializer.data

        self.assertEqual(data['username'], user.username)
        self.assertTrue(user.check_password('test_password'))

    def test_token_fields_content(self):
        token = {
            "access": "xyz",
            "refresh": "abc",
        }
        serializer = TokenSerializer(data=token)

        self.assertTrue(serializer.is_valid())
        self.assertTrue(serializer.data['access'], token['access'])
        self.assertTrue(serializer.data['refresh'], token['refresh'])
