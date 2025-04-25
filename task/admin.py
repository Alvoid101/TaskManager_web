from django.contrib import admin
from .models import Task, Link, Category

# Register your models here.
admin.site.register(Task)
admin.site.register(Link)
admin.site.register(Category)