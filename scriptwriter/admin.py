from django.contrib import admin
from .models import ScriptProject

@admin.register(ScriptProject)
class ScriptProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'created_at', 'updated_at')
    list_filter = ('genre', 'created_at')
    search_fields = ('title', 'logline', 'content')
    readonly_fields = ('created_at', 'updated_at')

