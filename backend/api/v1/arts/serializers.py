from rest_framework import serializers

from arts.models import Category, Color, Event, Orientation, Size, Style


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ("id", "title", "image", "begin", "end")


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
