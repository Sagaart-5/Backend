from django.contrib import admin

from .models import Art, Category, Color, Orientation, Size, Style


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
        "author_name",
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
                    "author_name",
                    ("title", "year"),
                    "price",
                    ("category", "size", "style"),
                    ("orientation", "color"),
                    "image",
                )
            },
        ),
    )
    search_fields = ("title", "author_name")
    search_help_text = "Поиск по названию или имени автора"
    list_filter = ("year", "category", "size", "style", "orientation", "color")

