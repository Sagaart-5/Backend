from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from arts import urls as arts_urls
from arts.views import sell_art_object, evaluate_art_object, purchase_art_object


urlpatterns = [
    path("v1/", include("api.v1.urls")),
    path("arts/", include(arts_urls)),
    path("sell/", sell_art_object, name="sell"),
    path("evaluation/", evaluate_art_object, name="evaluation"),
    path("purchase/", purchase_art_object, name="purchase"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
]
