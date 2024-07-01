from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django_cleanup.cleanup import cleanup_select

from .validators import validate_year


User = get_user_model()


class NameModel(models.Model):
    """Абстрактная модель с названием"""

    name = models.CharField(
        "Название", max_length=50, unique=True, db_index=True
    )

    class Meta:
        abstract = True
        ordering = ("name",)

    def __str__(self):
        return self.name


class TypeModel(models.Model):
    """Абстрактная модель с типом"""

    type = models.CharField("Тип", max_length=50, unique=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ("type",)

    def __str__(self):
        return self.type


class Category(NameModel):
    objects = None

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Size(NameModel):
    objects = None

    class Meta:
        verbose_name = "Размер"
        verbose_name_plural = "Размеры"


class Style(NameModel):
    objects = None

    class Meta:
        verbose_name = "Стиль"
        verbose_name_plural = "Стили"


class Orientation(TypeModel):
    objects = None

    class Meta:
        verbose_name = "Ориентация"
        verbose_name_plural = "Ориентации"


class Color(TypeModel):
    objects = None

    class Meta:
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"


@cleanup_select
class Author(models.Model):
    class Gender(models.TextChoices):
        MALE = "М", "Male"
        FEMALE = "Ж", "Female"

    name = models.CharField("Автор объекта", max_length=255)
    image = models.ImageField(
        "Фото", upload_to="artists/%Y/%m/", null=True, blank=True
    )
    description = models.TextField("Описание", blank=True)
    gender = models.CharField("Пол", choices=Gender.choices, max_length=6)
    country = models.CharField("Страна", max_length=50)
    birth_date = models.DateField("Дата рождения")
    death_date = models.DateField("Дата смерти", blank=True, null=True)

    class Meta:
        verbose_name = "Автор картины"
        verbose_name_plural = "Авторы картин"

    def __str__(self):
        return self.name


class Show(NameModel):
    class Meta:
        verbose_name = "Показ"
        verbose_name_plural = "Показы"


@cleanup_select
class Art(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, verbose_name="Автор"
    )
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, verbose_name="Категория"
    )
    size = models.ForeignKey(
        Size, on_delete=models.PROTECT, verbose_name="Размер"
    )
    style = models.ForeignKey(
        Style, on_delete=models.PROTECT, verbose_name="Стиль"
    )
    orientation = models.ForeignKey(
        Orientation, on_delete=models.PROTECT, verbose_name="Ориентация"
    )
    color = models.ForeignKey(
        Color, on_delete=models.PROTECT, verbose_name="Цвет"
    )

    author = models.ForeignKey(
        Author, verbose_name="Автор объекта", on_delete=models.PROTECT
    )
    title = models.CharField("Название", max_length=255)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField("Фото", upload_to="arts/%Y/%m/%d/")
    price = models.PositiveIntegerField(
        "Цена",
        validators=[MinValueValidator(1)],
        db_index=True,
    )
    appraisal_price = models.PositiveIntegerField(
        "Оценочная цена",
        validators=[MinValueValidator(1)],
        null=True,
        blank=True,
    )
    year = models.SmallIntegerField(
        "Год создания объекта",
        validators=[MinValueValidator(100), validate_year],
    )
    created = models.DateField("Создан", auto_now_add=True)
    sold = models.BooleanField(
        "Объект продан",
        default=False,
    )
    popular = models.PositiveSmallIntegerField("Популярность", default=0)
    solo_shows = models.ManyToManyField(
        Show, blank=True, related_name="solo_arts"
    )
    group_shows = models.ManyToManyField(
        Show, blank=True, related_name="group_arts"
    )

    class Meta:
        verbose_name = "Арт-объект"
        verbose_name_plural = "Арт-объекты"
        default_related_name = "arts"

    def __str__(self):
        return f"Арт-объект {self.title!r} - {self.year} создания."


@cleanup_select
class Event(models.Model):
    title = models.CharField("Название", max_length=150)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField("Фото", upload_to="events/%Y/")
    link = models.URLField("Ссылка")
    begin = models.DateField("Начало события")
    end = models.DateField("Конец события")

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "События"
        ordering = ["begin", "end"]

    def __str__(self):
        return f"{self.title}, {self.begin} - {self.end}"

    def clean(self):
        if self.end < self.begin:
            self.end, self.begin = self.begin, self.end

    # TODO: Проверять ли чтобы не создавать задним числом события?


class Appraisal(models.Model):
    class Status(models.TextChoices):
        not_started = "not_started", "Not started"
        in_progress = "in_progress", "In Progress"
        completed = "completed", "Completed"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    art = models.ForeignKey(Art, on_delete=models.CASCADE)
    status = models.CharField(
        "Статус",
        max_length=15,
        choices=Status.choices,
        default=Status.not_started,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "art"], name="unique_art_user"
            )
        ]
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
        default_related_name = "appraisals"

    def __str__(self):
        return (
            f"Оценка {self.art!r} "
            f"пользователем {self.user!r} "
            f"- статус {self.status!r}"
        )
