
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator
from django.db import models


class CustomUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        user = self.create_user(
            email,
            password=password,
            **extra_fields
        )

        user.is_admin = True
        user.save(using=self._db)

        return user


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    first_name = None
    last_name = None
    date_joined = None

    user_id = models.AutoField(primary_key=True)

    email = models.EmailField(unique=True)
    username = models.CharField(
        max_length=50
    )

    phone_num = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                r"^01([0|1|6|7|8|9])-?([0-9]{3,4})-?([0-9]{4})$",
                message="양식에 맞춰 휴대폰번호를 입력해주세요 EX) 010-1234-1234"
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
    birthdate = models.DateField(blank=True, null=True)
    position = models.CharField(max_length=50, blank=True)
    department = models.CharField(max_length=50)
    point = models.CharField(max_length=10, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

