from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    first_name = None
    last_name = None
    date_joined = None

    email = models.EmailField(primary_key=True)
    username = models.CharField(
        max_length=50
    )

    phone_num = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                r"^01([0|1|6|7|8|9])-?([0-9]{3,4})-?([0-9]{4})$",
                message="휴대폰번호를 입력해주세요"
            ),
    ],
    help_text="입력예) 010-1234-1234")
    gender = models.CharField(
        max_length=1,
        choices=[
            ("M", "Male"),
            ("F", "Female"),
        ],
        blank=True)
    birthdate = models.DateField(blank=True)
    position = models.CharField(max_length=50, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)