from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    email = models.EmailField(unique=True)

    first_name = None
    last_name = None
    username = models.CharField(
        max_length=50
    )

    gender = models.CharField(
        max_length=1,
        choices=[
            ("M", "Male"),
            ("F", "Female"),
        ],
        blank=True)
    birthdate = models.DateField(blank=True)
    position = models.CharField(max_length=50, blank=True)
