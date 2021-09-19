from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from . import constants


class CreatedUpdatedMixin:
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ApiUser(AbstractUser, CreatedUpdatedMixin):

    def __str__(self):
        return self.username


# Generated User
class User(models.Model, CreatedUpdatedMixin):
    gender = models.CharField(choices=constants.gender, max_length=settings.SHORT_TEXT_LENGTH)
    first_name = models.CharField(max_length=settings.SHORT_TEXT_LENGTH)
    last_name = models.CharField(max_length=settings.SHORT_TEXT_LENGTH)
    country = models.CharField(max_length=settings.MEDIUM_TEXT_LENGTH)
    city = models.CharField(max_length=settings.MEDIUM_TEXT_LENGTH)
    email = models.EmailField(max_length=settings.MAX_EMAIL_LENGTH)
    username = models.CharField(max_length=settings.SHORT_TEXT_LENGTH)
    phone = models.CharField(validators=[constants.phone_regex], max_length=settings.PHONE_NUM_LENGTH)
    picture = models.ImageField()
    creator = models.ForeignKey(ApiUser, on_delete=models.CASCADE, related_name='generated_users')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
