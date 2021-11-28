from django.contrib.auth import get_user_model
from django.test import TestCase


def sample_api_user():
    return get_user_model().objects.create_user(
        username='test_user',
        password='test_pass'
    )


class TestModels(TestCase):

    def test_create_api_user(self):
        user = sample_api_user()
        password = 'test_pass'

        self.assertEqual(user.username, 'test_user')
        self.assertTrue(user.check_password(password))
