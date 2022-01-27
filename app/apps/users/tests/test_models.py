from django.test import TestCase

from apps.users.models import User
from apps.api_users.models import ApiUser


def sample_api_user():
    return ApiUser.objects.create(
        username="test_api@user.com",
        password="test_pass123"
    )


def sample_user():
    return User.objects.create(
        gender="male",
        first_name="Mateusz",
        last_name="Perkins",
        country="United Kingdom",
        city="Opole",
        email="mario.perkins@example.com",
        username="organicgoose823",
        phone="0716-846-384"
    )


class TestModels(TestCase):

    def test_create_new_user(self):
        email = "mario.perkins@example.com"
        phone = "0716-846-384"
        user = sample_user()

        self.assertEqual(user.email, email)
        self.assertEqual(user.phone, phone)

    def test_str_user(self):
        user = sample_user()

        self.assertEqual(str(user), f"{user.first_name} {user.last_name}")
