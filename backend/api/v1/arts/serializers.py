from django.utils.translation import gettext_lazy as _
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from arts.models import Art, Category, Color, Event, Orientation, Size, Style, Author


def month_to_str(date):
    return _(date.strftime("%B"))


class EventSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ("id", "title", "link", "image", "date")

    def get_date(self, event) -> str:
        begin = event.begin
        end = event.end
        if begin.month == end.month:
            return f"{begin.day}-{end.day} {month_to_str(begin)}"
        return (
            f"{begin.day} {month_to_str(begin)}-{end.day} {month_to_str(end)}"
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ("id", "name")


class StyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Style
        fields = ("id", "name")


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ("id", "type")


class OrientationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orientation
        fields = ("id", "type")


class ArtAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("id", "name", "description")


class ArtListSerializer(serializers.ModelSerializer):
    art_author = serializers.CharField(source="art_author.name")

    class Meta:
        model = Art
        fields = ("id", "title", "art_author", "image", "price")


class ArtDetailSerializer(serializers.ModelSerializer):
    art_author = ArtAuthorSerializer()
    category = serializers.CharField(source="category.name")
    size = serializers.CharField(source="size.name")
    style = serializers.CharField(source="style.name")
    orientation = serializers.CharField(source="orientation.type")
    color = serializers.CharField(source="color.type")

    class Meta:
        model = Art
        fields = (
            "id",
            "art_author",
            "title",
            "image",
            "price",
            "category",
            "size",
            "style",
            "orientation",
            "color",
        )


class ArtCreateSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Art
        fields = (
            "id",
            "art_author",
            "title",
            "image",
            "price",
            "category",
            "size",
            "style",
            "orientation",
            "color",
            "year",
        )
