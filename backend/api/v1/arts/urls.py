from rest_framework.routers import SimpleRouter

from . import views


router = SimpleRouter()
router.register("arts", views.ArtViewSet, basename="arts")
router.register("categories", views.CategoryViewSet, basename="categories")
router.register("colors", views.ColorViewSet, basename="colors")
router.register("events", views.EventViewSet, basename="events")
router.register(
    "orientations", views.OrientationViewSet, basename="orientations"
)
router.register("sizes", views.SizeViewSet, basename="sizes")
router.register("styles", views.StyleViewSet, basename="styles")
