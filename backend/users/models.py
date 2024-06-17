from django.contrib.auth.models import AbstractUser
from django.db import models

from .manager import CustomUserManager


class CustomUser(AbstractUser):
    """Модель Пользователя."""
    # Когда перейдем на PostgreSQL установить id
    # id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    username = None
    first_name = models.CharField(
        "Имя пользователя",
        unique=False,
        max_length=50,
        blank=False,
        null=False,
    )
    last_name = models.CharField(
        "Фамилия пользователя",
        unique=False,
        max_length=50,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        "Почта",
        unique=True,
        max_length=254,
        blank=False,
        null=False,
    )
    phone_number = models.CharField(
        "Номер телефон",
        max_length=12,
        unique=True,
        blank=False,
        null=False,
    )
    password = models.CharField(
        "Пароль",
        max_length=128,
        blank=False,
        null=False,
    )

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("email",)

    def __str__(self):
        return f"Почта - {self.email}, телефон - {self.phone_number} пользователя."
