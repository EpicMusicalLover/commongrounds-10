from django.contrib import admin
from .models import CommissionType, Commission


class CommissionTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )
    search_fields = ("name",)
    ordering = ("name",)


class CommissionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "people_required",
    )
    search_fields = (
        "title",
        "description",
    )
    ordering = ("created_on",)


admin.site.register(CommissionType, CommissionTypeAdmin)
admin.site.register(Commission, CommissionAdmin)
