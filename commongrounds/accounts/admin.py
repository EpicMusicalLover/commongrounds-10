from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "display_name", "email", "role")
    search_fields = ("display_name", "email")
    list_filter = ("role",)


admin.site.register(Profile, ProfileAdmin)
