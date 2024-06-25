from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from arts.models import Category, Color, Event, Orientation, Size, Style


class EventSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ("id", "title", "link", "image", "date")

    def get_date(self, event) -> str:
        begin = event.begin
        end = event.end
        month_to_str = lambda d: _(d.strftime("%B"))
        if begin.month == end.month:
            return f"{begin.day}-{end.day} {month_to_str(begin)}"
        return f"{begin.day} {month_to_str(begin)}-{end.day} {month_to_str(end)}"


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
