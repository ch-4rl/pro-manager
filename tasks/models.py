from django.db import models
from django.contrib.auth.models import User
from projects.models import Project

class Task(models.Model):
    STATUS_CHOICES = [
        ("TODO", "To Do"),
        ("DOING", "Doing"),
        ("DONE", "Done"),
    ]

    PRIORITY_CHOICES = [
        ("LOW", "Low"),
        ("MED", "Medium"),
        ("HIGH", "High"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="TODO")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="MED")
    due_date = models.DateField(null=True, blank=True)
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="tasks")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.task}"

# Create your models here.
