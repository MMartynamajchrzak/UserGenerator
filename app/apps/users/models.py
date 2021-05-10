from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Users(User):
    phone_regex = RegexValidator(regex=r'^\+\d{7,15}$', message='First input country code eg.(+48), then the number.')
    phone_num = models.CharField(validators=[phone_regex], max_length=16)
    address = models.CharField(max_length=500)
