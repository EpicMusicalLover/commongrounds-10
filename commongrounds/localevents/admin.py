from django.contrib import admin
from .models import Event, EventType


class EventTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )
    search_fields = ("name",)
    ordering = ("name",)


class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "organizer",
        "event_image",
        "description",
        "location",
        "start_time",
        "end_time",
        "event_capacity",
        "status",
    )
    list_filter = (
        "created_on",
        "category",
    )
    search_fields = (
        "title",
        "location",
    )
    ordering = ("-created_on",)


admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Event, EventAdmin)
