from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description"]


class AddMemberForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        help_text="Enter the Django username to add",
    )    

