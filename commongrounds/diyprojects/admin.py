from django.contrib import admin
from .models import ProjectCategory, Project


class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    ordering = ("name",)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_on")
    search_fields = ("title", "description")
    ordering = ("-created_on",)


admin.site.register(ProjectCategory, ProjectCategoryAdmin)
admin.site.register(Project, ProjectAdmin)
