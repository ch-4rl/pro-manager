from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm
from tasks.forms import TaskForm

@login_required(login_url="/admin/login/")
def dashboard(request):
    projects = Project.objects.filter(owner=request.user)
    return render(request, "projects/dashboard.html", {"projects": projects})

@login_required(login_url="/admin/login/")
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect("project_detail", project_id=project.id)
    else:
        form = TaskForm()

    tasks = project.tasks.all().order_by("-created_at")
    return render(request, "projects/project_detail.html", {"project": project, "tasks": tasks, "form": form,})

@login_required(login_url="/admin/login/")
def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect("dashboard")
    else:
        form = ProjectForm()

    return render(request, "projects/create_project.html", {"form": form})

# Create your views here.
