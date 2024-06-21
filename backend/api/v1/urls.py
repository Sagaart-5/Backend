from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .users import views


router = SimpleRouter()
router.register("users", views.CustomUserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("", include("djoser.urls.jwt")),
]
