from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from arts.models import Art, Category, Color, Event, Orientation, Size, Style
from .filters import ArtsFilterSet
from .paginations import ArtsPagination
from .serializers import (
    ArtCreateSerializer,
    ArtDetailSerializer,
    ArtListSerializer,
    CategorySerializer,
    ColorSerializer,
    EventSerializer,
    OrientationSerializer,
    SizeSerializer,
    StyleSerializer,
)
from .viewsets import ListViewSet, ReadOrCreateViewSet


ARTS_TAG = "Arts"

EVENTS_LIMIT = 8


@extend_schema(tags=[ARTS_TAG])
class ArtViewSet(ReadOrCreateViewSet):
    queryset = Art.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = ArtsPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ArtsFilterSet

    def get_serializer_class(self):
        if self.action == "list":
            return ArtListSerializer
        elif self.action == "create":
            return ArtCreateSerializer
        return ArtDetailSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@extend_schema(tags=[ARTS_TAG])
class CategoryViewSet(ListViewSet):
    queryset = Category.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer


@extend_schema(tags=[ARTS_TAG])
class ColorViewSet(ListViewSet):
    queryset = Color.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ColorSerializer


@extend_schema(tags=[ARTS_TAG])
class EventViewSet(ListViewSet):
    permission_classes = [AllowAny]
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(end__gte=timezone.now())[:EVENTS_LIMIT]

    def get_object(self):
        return get_object_or_404(Event, pk=self.kwargs["pk"])


@extend_schema(tags=[ARTS_TAG])
class OrientationViewSet(ListViewSet):
    queryset = Orientation.objects.all()
    permission_classes = [AllowAny]
    serializer_class = OrientationSerializer


@extend_schema(tags=[ARTS_TAG])
class SizeViewSet(ListViewSet):
    queryset = Size.objects.all()
    permission_classes = [AllowAny]
    serializer_class = SizeSerializer


@extend_schema(tags=[ARTS_TAG])
class StyleViewSet(ListViewSet):
    queryset = Style.objects.all()
    permission_classes = [AllowAny]
    serializer_class = StyleSerializer
