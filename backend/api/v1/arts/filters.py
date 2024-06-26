from django.db.models import Q
from django_filters.rest_framework import CharFilter, FilterSet

from arts.models import Art


class ArtsFilterSet(FilterSet):
    price = CharFilter(method="get_price")
    category = CharFilter(method="add_filter", field_name="category__name")
    orientation = CharFilter(
        method="add_filter", field_name="orientation__type"
    )
    color = CharFilter(method="add_filter", field_name="color__type")
    style = CharFilter(method="add_filter", field_name="style__name")
    size = CharFilter(method="add_filter", field_name="size__name")

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

    @staticmethod
    def add_filter(queryset, name, value):
        q = Q()
        if value:
            for params in value.split(","):
                q |= Q(**{name: params})
        return queryset.filter(q)
