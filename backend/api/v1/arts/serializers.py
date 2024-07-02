from django.utils.translation import gettext_lazy as _
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from arts.models import Appraisal, Art, Author, Event


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


class ArtCreateSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Art
        fields = (
            "id",
            "author",
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


class ArtShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Art
        fields = ("id", "title")


class AppraisalSerializer(serializers.ModelSerializer):
    user = serializers.CurrentUserDefault()
    art = ArtShortSerializer(read_only=True)

    class Meta:
        model = Appraisal
        fields = ("user", "art", "status")


class ArtSearchFieldsSerializer(serializers.Serializer):
    category = serializers.ListField()
    styles = serializers.ListField()
    sizes = serializers.ListField()
    orientations = serializers.ListField()
    colors = serializers.ListField()


class ArtWithoutAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Art
        fields = (
            "id",
            "title",
            "image",
            "price",
        )


class AuthorArtSerializer(serializers.ModelSerializer):
    about = serializers.CharField(source="description")
    image = Base64ImageField()
    arts = ArtWithoutAuthorSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ("id", "name", "about", "image", "arts")


class ArtListSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.name")
    size = serializers.CharField(source="size.name")
    style = serializers.CharField(source="style.name")

    class Meta:
        model = Art
        fields = (
            "id",
            "title",
            "author",
            "image",
            "price",
            "style",
            "size",
            "year",
            "popular",
        )


class ArtSerializer(ArtListSerializer):
    author = AuthorArtSerializer()
    category = serializers.CharField(source="category.name")
    orientation = serializers.CharField(source="orientation.type")
    color = serializers.CharField(source="color.type")

    class Meta(ArtListSerializer.Meta):
        fields = (
            "id",
            "title",
            "author",
            "image",
            "price",
            "category",
            "size",
            "style",
            "orientation",
            "color",
            "year",
            "description",
            "popular",
        )
