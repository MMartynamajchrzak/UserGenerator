import factory

from .. import models


class ApiUserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: f"test_user{n}")
    password = factory.PostGenerationMethodCall("set_password", "password")
    is_staff = False
    is_superuser = False

    class Meta:
        model = models.ApiUser


class UserFactory(factory.django.DjangoModelFactory):
    gender = factory.Faker("gender")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    country = factory.Faker("country")
    city = factory.Faker("city")
    email = factory.Sequence(lambda n: f"{UserFactory.first_name}{n}@email.com")
    username = factory.Sequence(lambda n: f"test_user{n}")
    phone = factory.Sequence(lambda n: "123-555-%04d" % n)
    picture = factory.django.ImageField(width=250, height=250)
    creator = factory.SubFactory(ApiUserFactory)

    class Meta:
        model = models.User
