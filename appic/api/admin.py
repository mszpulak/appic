from django.contrib import admin

from django.contrib import admin

from .models import Artist, Event, Performance

admin.site.register(Artist)
admin.site.register(Event)
admin.site.register(Performance)
