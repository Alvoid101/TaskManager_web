from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class TaskCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_categories')
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Task_Categories"

class Link(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='links')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='links')
    name = models.CharField(max_length=200)
    content = models.TextField()
    
    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=70)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(TaskCategory, related_name='tasks')  # <-- Aquí
    delivery_date = models.DateTimeField()
    finished = models.BooleanField(default=False)

    def __str__(self):
        return self.title