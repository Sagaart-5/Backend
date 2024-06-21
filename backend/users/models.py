from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .manager import CustomUserManager


class CustomUser(AbstractUser):
    """Модель Пользователя."""

    username = None
    first_name = models.CharField(
        "Имя пользователя",
        max_length=50,
    )
    last_name = models.CharField(
        "Фамилия пользователя",
        max_length=50,
    )
    email = models.EmailField(
        "Почта",
        unique=True,
        max_length=254,
    )
    phone_number = PhoneNumberField(
        "Номер телефон",
        max_length=12,
        unique=True,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number", "first_name", "last_name"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("email",)

    def __str__(self):
        return (
            f"Почта - {self.email}, "
            f"телефон - {self.phone_number} пользователя."
        )
