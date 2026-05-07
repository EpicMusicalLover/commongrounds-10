from django.contrib import admin
from .models import Event, EventType, EventSignup

@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )
    search_fields = ("name",)
    ordering = ("name",)

@admin.register(Event)
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

@admin.register(EventSignup)
class EventSignupAdmin(admin.ModelAdmin):
    list_display = ('event', 'user_registrant', 'new_registrant')