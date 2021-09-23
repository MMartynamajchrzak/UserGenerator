from django.contrib.auth.models import AbstractUser

from apps.users.models import CreatedUpdatedMixin


class ApiUser(AbstractUser, CreatedUpdatedMixin):

    def __str__(self):
        return self.username
