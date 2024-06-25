from django.urls import path

from .views import ArtViewSet


urlpatterns = [
    path("", ArtViewSet.as_view({"get": "list"}), name="arts-list"),
]
