from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.

class List(models.Model):
    """Represents a category or list (e.g., Work, Personal)"""
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=7, default="#000000")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
class Tag(models.Model):
    """Tags for categorizing tasks (e.g., Urgent, Priority)"""
    name = models.CharField(max_length=100,unique=True)
    color = models.CharField(max_length=7, default="#000000")
    slug = models.SlugField(unique=True, blank=True)
    
    def __str__(self):
        return self.name 
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Task(models.Model):
    """Main task model"""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(null=True, blank=True, db_index=True)
    is_completed = models.BooleanField(default=False, db_index=True)
    is_deleted = models.BooleanField(default=False)
    list = models.ForeignKey(List, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    tags = models.ManyToManyField(Tag, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ['-due_date', '-created_at']
    
    def __str__(self):
        return self.title
    
    
    