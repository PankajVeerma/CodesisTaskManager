from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "status", "created_at")
    list_filter = ("status", "owner")
    search_fields = ("title", "description", "owner__email")
    ordering = ("-created_at",)

admin.site.register(Task, TaskAdmin)
