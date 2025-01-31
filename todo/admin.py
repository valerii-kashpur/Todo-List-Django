from django.contrib import admin

from todo.models import Tag, Task


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("content", "created_at", "deadline", "is_done", "display_tags")
    search_fields = ("content",)
    filter_horizontal = ("tags",)

    def display_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())

    display_tags.short_description = "Tags"
