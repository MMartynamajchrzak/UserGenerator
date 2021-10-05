from django.contrib.auth.models import AbstractUser
from django.db import models


class CreatedUpdatedMixin:
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ApiUser(AbstractUser, CreatedUpdatedMixin):

    def __str__(self):
        return self.username
