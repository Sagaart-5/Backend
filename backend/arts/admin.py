from django.contrib import admin

from .models import (
    Appraisal,
    Art,
    Author,
    Category,
    Color,
    Event,
    Orientation,
    Show,
    Size,
    Style,
)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Category, Size, Show, Style)
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
        "author",
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
                    "author",
                    ("title", "year", "popular"),
                    "description",
                    "price",
                    ("category", "size", "style"),
                    ("orientation", "color"),
                    "solo_shows",
                    "group_shows",
                    "image",
                    "user",
                )
            },
        ),
    )
    filter_horizontal = ("solo_shows", "group_shows")
    raw_id_fields = ("user", "author")
    search_fields = ("title", "author")
    search_help_text = "Поиск по названию или имени автора"
    list_filter = ("year", "category", "size", "style", "orientation", "color")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "begin", "end")


@admin.register(Appraisal)
class AppraisalAdmin(admin.ModelAdmin):
    raw_id_fields = ("user", "art")
