from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    avatar = models.ImageField(
        upload_to='users/avatars/',
        default=None,
        null=True
    )

    def __str__(self):
        return self.username
