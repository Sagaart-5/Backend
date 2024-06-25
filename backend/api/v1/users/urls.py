from rest_framework.routers import SimpleRouter

from . import views


router = SimpleRouter()
router.register("users", views.CustomUserViewSet, basename="users")
