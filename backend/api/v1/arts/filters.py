from django.db.models import Q
from django_filters.rest_framework import CharFilter, FilterSet

from arts.models import Art


class ArtsFilterSet(FilterSet):
    price = CharFilter(method="get_price")

    class Meta:
        model = Art
        fields = ["category", "orientation", "style", "size", "color"]

    def get_price(self, queryset, name, value):
        q_price = Q()
        if value:
            for price_range in value.split(","):
                min_price, max_price = price_range.strip().split("-")
                q_price |= Q(price__gte=min_price, price__lte=max_price)
        return queryset.filter(q_price)
