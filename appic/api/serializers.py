import rest_framework.exceptions
from rest_framework import serializers
from .models import Artist, Performance, Event, TaskReport
import logging

logger = logging.getLogger("api")


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class PerformanceSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    artist = ArtistSerializer(many=True, read_only=True)

    class Meta:
        model = Performance
        fields = "__all__"


class PerformanceCUSerializer(serializers.ModelSerializer):
    event = serializers.SlugRelatedField(
        slug_field="name", queryset=Event.objects.all()
    )
    artist = serializers.SlugRelatedField(
        many=True, slug_field="name", queryset=Artist.objects.all()
    )

    class Meta:
        model = Performance
        fields = "__all__"

    def create(self, validated_data: dict):
        logger.info("create %s", validated_data)
        artist = validated_data.pop("artist")
        event = validated_data.pop("event")

        performance = Performance.objects.create(**validated_data, event=event)
        performance.artist.set(artist)
        return performance

    def update(self, instance, validated_data: dict):
        logger.info("create %s", validated_data)
        artist = validated_data.pop("artist", instance.artist)
        event = validated_data.pop("event", instance.event)

        instance.start = validated_data.get("start", instance.start)
        instance.end = validated_data.get("end", instance.end)
        instance.event = event
        instance.artist.set(artist)
        instance.save()
        return instance

    def validate(self, attrs):
        logger.info("attrs %s", attrs)
        if not attrs["start"] < attrs["end"]:
            raise rest_framework.exceptions.ValidationError("End earlier than start")

        if attrs["event"].start > attrs["start"]:
            raise rest_framework.exceptions.ValidationError(
                "performance start not valid"
            )
        if attrs["event"].end < attrs["start"]:
            raise rest_framework.exceptions.ValidationError(
                "performance start not valid"
            )

        if attrs["event"].end > attrs["end"]:
            raise rest_framework.exceptions.ValidationError(
                "performance start not valid"
            )
        if attrs["event"].start < attrs["end"]:
            raise rest_framework.exceptions.ValidationError(
                "performance start not valid"
            )

        return attrs


class EventPerformanceSerializer(serializers.ModelSerializer):
    performances = PerformanceSerializer(many=True)

    class Meta:
        model = Event
        fields = ["performances", "name", "start", "end"]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskReport
        fields = "__all__"
