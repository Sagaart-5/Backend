from django.urls import include, path

from .arts.urls import router as art_router
from .users.urls import router as user_router


urlpatterns = [
    path("", include(art_router.urls)),
    path("", include(user_router.urls)),
    path("", include("djoser.urls.jwt")),
]
