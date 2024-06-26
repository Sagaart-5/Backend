from django.contrib import admin

from .models import (
    Art,
    Author,
    Category,
    Color,
    Event,
    Orientation,
    Size,
    Style,
)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Category, Size, Style)
class NamedAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Color, Orientation)
class TypedAdmin(admin.ModelAdmin):
    list_display = ("type",)
    search_fields = ("type",)


@admin.register(Art)
class ArtAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "art_author",
        "year",
        "price",
        "category",
        "size",
        "style",
        "orientation",
        "color",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "art_author",
                    ("title", "year"),
                    "price",
                    ("category", "size", "style"),
                    ("orientation", "color"),
                    "image",
                    "author",
                )
            },
        ),
    )
    search_fields = ("title", "art_author")
    search_help_text = "Поиск по названию или имени автора"
    list_filter = ("year", "category", "size", "style", "orientation", "color")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "begin", "end")
