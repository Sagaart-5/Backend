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
class Art(models.Model):
    # author = models.ForeignKey(
    #     User, on_delete=models.PROTECT, verbose_name="Автор"
    # )
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

    author_name = models.CharField("Автор объекта", max_length=255)
    title = models.CharField("Название", max_length=255)
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
