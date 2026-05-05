from django.contrib.auth.models import AbstractUser
from django.db.models import TextChoices
from django.db.models.fields import CharField

from apps.models.managers import CustomUserManager


class User(AbstractUser):
    class Role(TextChoices):
        ADMIN = 'admin', 'Admin'
        AUTHOR = 'author', 'Author'
        READER = 'reader', 'Reader'

    role = CharField(max_length=15, choices=Role.choices, default=Role.READER)

    objects = CustomUserManager()