from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class CustomUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "password",
            "phone_number",
        )
        extra_kwargs = {"password": {"write_only": True}}


class CustomUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id",)
