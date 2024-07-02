from djoser.views import UserViewSet
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["users"])
class CustomUserViewSet(UserViewSet):
    pass
