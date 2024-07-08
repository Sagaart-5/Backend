# flake8:noqa
from .urls import *


urlpatterns += [
    path("__debug__/", include("debug_toolbar.urls")),
    path("auth/", include("rest_framework.urls")),
]
