from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """Менеджер модели пользователя."""

    use_in_migrations = True

    def create_user(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        **extra_fields,
    ):
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", False)

        """
        Создает и сохраняет пользователя с заданными данными.
        """

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        password: str,
        **extra_fields,
    ):

        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Суперпользователь должен быть is_superuser=True."
            )
        """
        Создает и сохраняет супер-пользователя с заданными данными.
        """

        user = self.create_user(
            first_name="Админ",
            last_name="@",
            email=email,
            password=password,
            **extra_fields,
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user
