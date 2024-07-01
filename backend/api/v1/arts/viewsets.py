from rest_framework import mixins, viewsets


class ListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class RetrieveViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pass


class ReadOrCreateViewSet(
    mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet
):
    pass
