import rest_framework.exceptions
from rest_framework import serializers
from .models import Artist, Performance, Event
import logging

logger = logging.getLogger("api")


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = "__all__"
        extra_kwargs = {
            "name": {"validators": []},
        }


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
        extra_kwargs = {
            "name": {"validators": []},
        }


class PerformanceSerializer(serializers.ModelSerializer):
    event = EventSerializer(
        partial=True,
    )
    artist = ArtistSerializer(many=True, partial=True)

    def create(self, validated_data):
        logger.info(validated_data)
        artist = validated_data.pop("artist")
        event = validated_data.pop("event")

        try:
            event = Event.objects.get(name=event["name"])
        except Event.DoesNotExist:
            raise rest_framework.exceptions.ValidationError("Event Not Found")

        artists_list = []
        try:
            for art in artist:
                artist = Artist.objects.get(name=art["name"])
                artists_list.append(artist)
        except Artist.DoesNotExist:
            raise rest_framework.exceptions.ValidationError("Artist Not Found")

        performance = Performance.objects.create(**validated_data, event=event)
        performance.artist.set(artists_list)
        return performance

    class Meta:
        model = Performance
        fields = "__all__"


class EventPerformanceSerializer(serializers.ModelSerializer):
    performances = PerformanceSerializer(many=True)

    class Meta:
        model = Event
        fields = ["performances", "name", "start", "end"]
