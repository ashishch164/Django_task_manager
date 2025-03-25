from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=False)
    username = models.CharField(max_length=15, unique=True)
    mobile = models.CharField(max_length=15, unique=True)
    role = models.IntegerField(default=1) # 0 = Admin, 1 = Regular User
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ]

    TASK_TYPES = [
        ('bug', 'Bug'),
        ('feature', 'Feature')
    ]

    name = models.CharField(max_length=255, null=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    task_type = models.CharField(max_length=20, choices=TASK_TYPES, default='feature')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class UserTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    weightage = models.IntegerField(default=1)  # Higher weightage means higher priority
    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['deadline', '-weightage']  # Highest weight first, then by deadline

    def __str__(self):
        return f"{self.user.name} -> {self.task.name}"