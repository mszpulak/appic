from django.db import models
import datetime
from django.utils.translation import gettext_lazy as _
import uuid


class Event(models.Model):
    name = models.CharField(max_length=200, unique=True)
    start = models.DateTimeField()
    end = models.DateTimeField()


class Artist(models.Model):
    class Genre(models.TextChoices):
        RAP = "RAP", _("RAP music")
        POP = "POP", _("POP music")

    name = models.CharField(max_length=200, unique=True)
    music_genre = models.CharField(max_length=200, choices=Genre, default=Genre.RAP)


class Performance(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="performances"
    )
    artist = models.ManyToManyField(Artist)
    start = models.DateTimeField()
    end = models.DateTimeField()


class TaskReport(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    result = models.JSONField(null=True)
