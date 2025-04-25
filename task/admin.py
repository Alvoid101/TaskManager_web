from django.contrib import admin
from .models import Task, Link, Category, TaskCategory

# Register your models here.
admin.site.register(Task)
admin.site.register(Link)
admin.site.register(Category)
admin.site.register(TaskCategory)