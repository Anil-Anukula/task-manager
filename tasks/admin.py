from django.contrib import admin
from .models import Task, Tag, List
# Register your models here.

admin.site.register(Task)
admin.site.register(Tag)
admin.site.register(List)