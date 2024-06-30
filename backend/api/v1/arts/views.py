from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from arts.models import (
    Art,
    Author,
    Category,
    Color,
    Event,
    Orientation,
    Size,
    Style,
)
from arts.tasks import get_appraisal_price
from .filters import ArtsFilterSet
from .paginations import ArtsPagination
from .serializers import (
    AppraisalSerializer,
    ArtCreateSerializer,
    ArtListSerializer,
    ArtSearchFieldsSerializer,
    ArtSerializer,
    AuthorArtSerializer,
    EventSerializer,
)
from .viewsets import ListViewSet, ReadOrCreateViewSet, RetrieveViewSet


ARTS_TAG = "Arts"

EVENTS_LIMIT = 8
MOST_POPULAR_LIMIT = 5


@extend_schema(tags=[ARTS_TAG])
class ArtViewSet(ReadOrCreateViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = ArtsPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ArtsFilterSet

    def get_serializer_class(self):
        if self.action in ("list", "most_popular"):
            return ArtListSerializer
        elif self.action == "create":
            return ArtCreateSerializer
        elif self.action == "art_search_fields":
            return ArtSearchFieldsSerializer
        return ArtSerializer

    def get_queryset(self):
        queryset = Art.objects.all()
        if self.action == "most_popular":
            return queryset.order_by("-popular")
        return queryset

    @action(detail=False, methods=["get"])
    def most_popular(self, request):
        qs = self.get_queryset()[:MOST_POPULAR_LIMIT]
        serializer = self.get_serializer(
            qs, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def appraisal(self, request, *args, **kwargs):
        get_appraisal_price.delay(kwargs.get("pk"), request.user.id)
        return JsonResponse({"status": "ok"})

    @action(
        detail=False,
        methods=["get"],
    )
    def art_search_fields(self, request):
        data = {
            "styles": list(Style.objects.all().values_list("name", flat=True)),
            "sizes": list(Size.objects.all().values_list("name", flat=True)),
            "categories": list(
                Category.objects.all().values_list("name", flat=True)
            ),
            "orientations": list(
                Orientation.objects.all().values_list("type", flat=True)
            ),
            "colors": list(Color.objects.all().values_list("type", flat=True)),
        }
        print(data)
        return JsonResponse(data, content_type="application/json")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=[ARTS_TAG])
class EventViewSet(ListViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(end__gte=timezone.now())[:EVENTS_LIMIT]

    def get_object(self):
        return get_object_or_404(Event, pk=self.kwargs["pk"])


class AppraisalViewSet(ListViewSet):
    serializer_class = AppraisalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.appraisals.all()


@extend_schema(tags=[ARTS_TAG])
class AuthorArtViewSet(RetrieveViewSet):
    queryset = Author
    serializer_class = AuthorArtSerializer
