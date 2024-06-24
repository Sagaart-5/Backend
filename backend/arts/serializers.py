from rest_framework import serializers

from .models import Art


class ArtSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Art."""

    class Meta:
        """Метакласс для указания модели и полей для сериализации."""

        model = Art
        fields = (
            "category",
            "size",
            "style",
            "orientation",
            "color",
            "author_name",
            "title",
            "image",
            "price",
            "year",
            "created",
        )


class SellArtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Art
        fields = "__all__"

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        return Art.objects.create(**validated_data)
