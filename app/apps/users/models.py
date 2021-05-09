from django.db import models
from django.contrib.auth.models import User


class Users(User):
    phone_num = models.IntegerField()
    address = models.CharField(max_length=500)
