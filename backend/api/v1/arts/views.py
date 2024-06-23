from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from arts.models import Category, Color, Event, Orientation, Size, Style
from .serializers import (
    CategorySerializer,
    ColorSerializer,
    EventSerializer,
    OrientationSerializer,
    SizeSerializer,
    StyleSerializer,
)


EVENTS_LIMIT = 12


@extend_schema(tags=["Arts"])
class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer


@extend_schema(tags=["Arts"])
class ColorViewSet(ReadOnlyModelViewSet):
    queryset = Color.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ColorSerializer


@extend_schema(tags=["Arts"])
class EventViewSet(ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(end__gte=timezone.now())[:EVENTS_LIMIT]

    def get_object(self):
        return get_object_or_404(Event, pk=self.kwargs["pk"])


@extend_schema(tags=["Arts"])
class OrientationViewSet(ReadOnlyModelViewSet):
    queryset = Orientation.objects.all()
    permission_classes = [AllowAny]
    serializer_class = OrientationSerializer


@extend_schema(tags=["Arts"])
class SizeViewSet(ReadOnlyModelViewSet):
    queryset = Size.objects.all()
    permission_classes = [AllowAny]
    serializer_class = SizeSerializer


@extend_schema(tags=["Arts"])
class StyleViewSet(ReadOnlyModelViewSet):
    queryset = Style.objects.all()
    permission_classes = [AllowAny]
    serializer_class = StyleSerializer
