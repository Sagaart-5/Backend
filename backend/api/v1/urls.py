from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .users.views import CustomUserViewSet

router = SimpleRouter()
router.register("users", CustomUserViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("", include("djoser.urls.jwt")),
]
