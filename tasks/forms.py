from django import forms
from .models import Task, Comment

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "status", "priority", "due_date"]

class TaskStatusForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["status"]            

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment     
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(attrs={"rows": 3}),
        }  

