from rest_framework.routers import DefaultRouter

api_router = DefaultRouter()
from .views import (
    EventViewSet,
    PerformanceViewSet,
    ArtistSerializerViewSet,
    EventPerformanceViewSet,
)

api_router.register(r"event", EventViewSet, basename="event")
api_router.register(r"performance", PerformanceViewSet, basename="performance")
api_router.register(r"artist", ArtistSerializerViewSet, basename="artist")
api_router.register(r"event_perf", EventPerformanceViewSet, basename="event_perf")
