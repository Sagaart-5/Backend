from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .arts import views as art_views
from .users import views as user_views


router = SimpleRouter()
router.register("users", user_views.CustomUserViewSet, basename="users")
router.register("categories", art_views.CategoryViewSet, basename="categories")
router.register("colors", art_views.ColorViewSet, basename="colors")
router.register("events", art_views.EventViewSet, basename="events")
router.register(
    "orientations", art_views.OrientationViewSet, basename="orientations"
)
router.register("sizes", art_views.SizeViewSet, basename="sizes")
router.register("styles", art_views.StyleViewSet, basename="styles")

urlpatterns = [
    path("", include(router.urls)),
    path("", include("djoser.urls.jwt")),
]
