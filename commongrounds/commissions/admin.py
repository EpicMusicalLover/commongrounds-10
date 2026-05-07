from django.contrib import admin
from .models import CommissionType, Commission, Job, JobApplication


class CommissionTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description",)
    search_fields = ("name",)
    ordering = ("name",)


class CommissionAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "people_required",)
    search_fields = ("title", "description",)
    ordering = ("created_on",)


class JobAdmin(admin.ModelAdmin):
    list_display = ("role", "status",)
    search_fields = ("role",)
    ordering = ("status",)


class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("applicant", "job", "status",)
    search_fields = ("applicant",)
    ordering = ("status",)


admin.site.register(CommissionType, CommissionTypeAdmin)
admin.site.register(Commission, CommissionAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
