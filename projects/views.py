from .models import Project, ProjectMembership
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm
from tasks.forms import TaskForm
from django.contrib.auth.models import User
from .forms import AddMemberForm
from django.views.decorators.http import require_POST

@login_required(login_url="/admin/login/")
def dashboard(request):
    projects = Project.objects.filter(
        Q(owner=request.user) | Q(memberships__user=request.user)
    ).distinct().order_by("-id")

    return render(request, "projects/dashboard.html", {"projects": projects})

@login_required(login_url="/admin/login/")
def project_detail(request, project_id):
    project = get_object_or_404(
     Project.objects.filter(
        Q(owner=request.user) | Q(memberships__user=request.user)
     ).distinct(),
     id=project_id
    )
    
    
    #Create task (POST)
    if request.method == "POST":
        form = TaskForm(request.POST)
        # Limit "assigned_to" to owner + members of this project
        allowed_users = User.objects.filter(
          Q(id=project.owner_id) | Q(project_memberships__project=project)
        ).distinct()
        form.fields["assigned_to"].queryset = allowed_users

        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect("project_detail", project_id=project.id)
    else:
        form = TaskForm()

    status = request.GET.get("status", "ALL")
    tasks_qs = project.tasks.all().order_by("-created_at")
    if status in {"TODO", "DOING", "DONE"}:
        tasks_qs = tasks_qs.filter(status=status)

    return render(request, "projects/project_detail.html", {"project": project, "tasks": tasks_qs, "form": form, "status_filter": status,  # so template can highlight active filter 
                                                            })

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


@login_required
def project_members(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)  # owner-only

    form = AddMemberForm(request.POST or None)
    message = None

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data["username"].strip()
            user = User.objects.filter(username=username).first()
            if not user:
                message = "User not found."
            elif user == project.owner:
                message = "Owner is already part of the project."
            else:
                ProjectMembership.objects.get_or_create(project=project, user=user)
                return redirect("project_members", project_id=project.id)

    members = User.objects.filter(project_memberships__project=project).distinct()

    return render(request, "projects/project_members.html", {
        "project": project,
        "members": members,
        "form": form,
        "message": message,
    })


@require_POST
@login_required
def remove_member(request, project_id, user_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)  # owner-only
    ProjectMembership.objects.filter(project=project, user_id=user_id).delete()
    return redirect("project_members", project_id=project.id)

# Create your views here.
