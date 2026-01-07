from django.db import models

class ScriptProject(models.Model):
    """Model for storing script projects"""
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
