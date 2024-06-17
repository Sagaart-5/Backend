from __future__ import annotations
import logging

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from .models import CustomUser


logger = logging.getLogger(__name__)


class AuthBackend(ModelBackend):
    supports_object_permissions = True
    supports_anonymous_user = True
    supports_inactive_user = True

    def get_user(self, user_id) -> CustomUser | None:
        print(user_id)
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None

    def authenticate(
            self, request, password, phone_number=None, username=None) -> CustomUser | None:
        print(request)
        print(phone_number, password, username)
        try:
            user: CustomUser = CustomUser.objects.get(
                Q(email=username) | Q(phone_number=username)
            )
            print(user.check_password(password))
        except CustomUser.DoesNotExist:
            return None

        if user.check_password(password):
            print("1")
            return user
        else:
            return None
