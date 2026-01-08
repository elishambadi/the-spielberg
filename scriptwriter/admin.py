from django.contrib import admin
from .models import ScriptProject, Character, Script, ScriptVersion, Scene, Job


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'created_at']
    list_filter = ['user', 'created_at']
    search_fields = ['name', 'personality', 'goals']


@admin.register(Script)
class ScriptAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'genre', 'tone', 'created_at', 'updated_at']
    list_filter = ['genre', 'tone', 'user', 'created_at']
    search_fields = ['title', 'logline']
    filter_horizontal = ['characters']


@admin.register(ScriptVersion)
class ScriptVersionAdmin(admin.ModelAdmin):
    list_display = ['script', 'version_number', 'created_at']
    list_filter = ['script', 'created_at']
    search_fields = ['script__title', 'notes']


@admin.register(Scene)
class SceneAdmin(admin.ModelAdmin):
    list_display = ['script_version', 'scene_number', 'setting', 'created_at']
    list_filter = ['script_version', 'created_at']
    search_fields = ['setting', 'goal', 'tension']


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['job_id', 'user', 'job_type', 'status', 'created_at', 'completed_at']
    list_filter = ['status', 'job_type', 'user', 'created_at']
    search_fields = ['job_id', 'prompt']
    readonly_fields = ['job_id', 'created_at', 'started_at', 'completed_at']


@admin.register(ScriptProject)
class ScriptProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'created_at', 'updated_at')
    list_filter = ('genre', 'created_at')
    search_fields = ('title', 'logline', 'content')
    readonly_fields = ('created_at', 'updated_at')


