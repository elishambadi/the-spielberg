from django.db import models
from django.contrib.auth.models import User


class Character(models.Model):
    """Model for storing character information"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='characters')
    name = models.CharField(max_length=200)
    personality = models.TextField(blank=True, help_text="Character personality traits")
    goals = models.TextField(blank=True, help_text="Character goals and motivations")
    voice = models.TextField(blank=True, help_text="Character voice and speaking style")
    backstory = models.TextField(blank=True, help_text="Character background")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.user.username})"


class Script(models.Model):
    """Model for storing script projects with versioning"""
    GENRE_CHOICES = [
        ('action', 'Action'),
        ('comedy', 'Comedy'),
        ('drama', 'Drama'),
        ('horror', 'Horror'),
        ('thriller', 'Thriller'),
        ('romance', 'Romance'),
        ('scifi', 'Science Fiction'),
        ('fantasy', 'Fantasy'),
        ('mystery', 'Mystery'),
        ('other', 'Other'),
    ]
    
    TONE_CHOICES = [
        ('light', 'Light'),
        ('serious', 'Serious'),
        ('dark', 'Dark'),
        ('comedic', 'Comedic'),
        ('dramatic', 'Dramatic'),
        ('suspenseful', 'Suspenseful'),
        ('inspirational', 'Inspirational'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scripts')
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, default='drama')
    tone = models.CharField(max_length=50, choices=TONE_CHOICES, default='dramatic')
    logline = models.TextField(blank=True)
    characters = models.ManyToManyField(Character, related_name='scripts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.title} ({self.user.username})"
    
    def get_latest_version(self):
        return self.versions.order_by('-version_number').first()


class ScriptVersion(models.Model):
    """Model for storing script versions"""
    script = models.ForeignKey(Script, on_delete=models.CASCADE, related_name='versions')
    version_number = models.PositiveIntegerField()
    content = models.TextField()
    notes = models.TextField(blank=True, help_text="Notes about this version")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-version_number']
        unique_together = ['script', 'version_number']
    
    def __str__(self):
        return f"{self.script.title} v{self.version_number}"


class Scene(models.Model):
    """Model for storing individual scenes"""
    script_version = models.ForeignKey(ScriptVersion, on_delete=models.CASCADE, related_name='scenes')
    scene_number = models.PositiveIntegerField()
    setting = models.CharField(max_length=500, help_text="Scene location and time")
    goal = models.TextField(help_text="What the scene aims to accomplish")
    tension = models.TextField(help_text="Source of conflict or tension")
    tone = models.CharField(max_length=50, blank=True, help_text="Specific tone for this scene")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['scene_number']
        unique_together = ['script_version', 'scene_number']
    
    def __str__(self):
        return f"Scene {self.scene_number}: {self.setting}"


class Job(models.Model):
    """Model for tracking async job status"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    JOB_TYPE_CHOICES = [
        ('script_generation', 'Script Generation'),
        ('scene_generation', 'Scene Generation'),
        ('script_refinement', 'Script Refinement'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    job_id = models.CharField(max_length=255, unique=True, db_index=True)
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    prompt = models.TextField()
    
    # Related objects
    script = models.ForeignKey(Script, on_delete=models.SET_NULL, null=True, blank=True, related_name='jobs')
    scene = models.ForeignKey(Scene, on_delete=models.SET_NULL, null=True, blank=True, related_name='jobs')
    
    # Results
    result = models.TextField(blank=True)
    error_message = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Job {self.job_id} - {self.status}"


class ScriptProject(models.Model):
    """Legacy model for backwards compatibility - consider migrating to Script"""
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100, blank=True)
    logline = models.TextField(blank=True)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return self.title

