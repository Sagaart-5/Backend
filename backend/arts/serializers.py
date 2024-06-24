from rest_framework import serializers

from .models import Art, Category, Size, Style, Orientation, Color


class ArtSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Art."""

    class Meta:
        """Метакласс для указания модели и полей для сериализации."""

        model = Art
        fields = (
            "id",
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
    """Сериализатор продажи объекта искусства."""
    class Meta:
        """Метакласс для указания модели и полей для сериализации."""

        model = Art
        fields = "__all__"

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        return Art.objects.create(**validated_data)


class EvaluationSerializer(serializers.ModelSerializer):
    """Сериализатор оценки стоимости объекта искусства."""

    objectId = serializers.IntegerField(required=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=True
    )
    size = serializers.PrimaryKeyRelatedField(
        queryset=Size.objects.all(),
        required=True
    )
    style = serializers.PrimaryKeyRelatedField(
        queryset=Style.objects.all(),
        required=True
    )
    orientation = serializers.PrimaryKeyRelatedField(
        queryset=Orientation.objects.all(),
        required=True
    )
    color = serializers.PrimaryKeyRelatedField(
        queryset=Color.objects.all(),
        required=True
    )

    class Meta:
        """Метакласс для указания модели и полей для сериализации."""

        model = Art
        fields = ["objectId", "category", "size", "style", "orientation", "color"]
