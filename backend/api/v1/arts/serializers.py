from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from arts.models import Category, Color, Event, Orientation, Size, Style


class EventSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ("id", "title", "link", "image", "date")

    def get_date(self, event):
        begin = event.begin
        end = event.end
        if begin.month == end.month:
            return f"{begin.day}-{end.day} {_(begin.strftime('%B'))}"
        return f"{begin.day} {_(begin.strftime('%B'))}-{end.day} {_(end.strftime('%B'))}"


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
