from rest_framework import viewsets
from .models import Artist, Event, Performance
from .serializers import (
    EventSerializer,
    PerformanceSerializer,
    ArtistSerializer,
    EventPerformanceSerializer,
)
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.settings import api_settings
from rest_framework_csv import renderers as r


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES) + (r.CSVRenderer,)


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.select_related("event").prefetch_related("artist")
    serializer_class = PerformanceSerializer


class ArtistSerializerViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class EventPerformanceViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.prefetch_related("performances").all()
    serializer_class = EventPerformanceSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = "__all__"
    search_fields = "__all__"
