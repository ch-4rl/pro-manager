from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .models import Task
from .forms import CommentForm, TaskStatusForm

@login_required(login_url="/admin/login/")
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # simple permission rule for now: only the project owner can view
    if task.project.owner != request.user:
        # behave like "not found" to avoid leaking existence
        return redirect("dashboard")   
    
    if request.method == "POST":
        if "status_submit" in request.POST:
            status_form = TaskStatusForm(request.POST, instance=task)
            if status_form.is_valid():
                status_form.save()
                return redirect("task_detail", task_id=task.id)
        else:
            comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
            return redirect("task_detail", task_id=task.id)
    else:
        status_form = TaskStatusForm(instance=task)
        comment_form = CommentForm()

    comments = task.comments.all().order_by("-created_at")

    return render(request, "tasks/task_detail.html", {
        "task": task,
        "comments": comments,
        "status_form": status_form,
        "form": comment_form,
    })

@require_POST
@login_required
def update_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Permission: only project owner can update
    if task.project.owner != request.user:
        return redirect("dashboard")

    status = request.POST.get("status")
    allowed = {choice[0] for choice in Task.STATUS_CHOICES}
    if status in allowed:
        task.status = status
        task.save()

    return redirect("project_detail", project_id=task.project.id) 
