from rest_framework import viewsets
from .models import Artist, Event, Performance, TaskReport
from .serializers import (
    EventSerializer,
    PerformanceSerializer,
    ArtistSerializer,
    PerformanceCUSerializer,
    EventPerformanceSerializer,
    TaskSerializer,
)
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.settings import api_settings
from rest_framework_csv import renderers as r
from rest_framework.decorators import action
from rest_framework.response import Response


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES) + (r.CSVRenderer,)


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.select_related("event").prefetch_related("artist")
    serializer_class = PerformanceSerializer

    def get_serializer_class(self):
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method." % self.__class__.__name__
        )

        if self.action in ["update", "create", "partial_update", "destroy"]:
            return PerformanceCUSerializer
        else:
            return self.serializer_class


class ArtistSerializerViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class EventPerformanceViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.prefetch_related("performances").all()
    serializer_class = EventPerformanceSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = "__all__"
    search_fields = "__all__"


class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TaskReport.objects.all()
    serializer_class = TaskSerializer

    @action(detail=False, methods=["post"])
    def get_csv(self, request):
        instance = TaskReport.objects.create()
        # run task csv_generator.delay(*args)
        # update instance
        url = self.reverse_action("detail", args=[str(instance.uuid)])

        return Response({"url": url})
