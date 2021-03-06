from django.test import TestCase

from apps.users.models import User
from apps.users.serializers import UserSerializer


class TestUserSerializer(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            gender="male",
            first_name="Mateusz",
            last_name="Perkins",
            country="United Kingdom",
            city="Opole",
            email="mario.perkins@example.com",
            username="organicgoose823",
            phone="0716-846-384"
        )

    def test_user_fields_content(self):
        serializer = UserSerializer(self.user)
        data = serializer.data

        self.assertEqual(data['first_name'], self.user.first_name)
        self.assertEqual(data['last_name'], self.user.last_name)
        self.assertEqual(data['phone'], self.user.phone)
