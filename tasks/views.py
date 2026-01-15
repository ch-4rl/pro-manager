from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import CommentForm

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # simple permission rule for now: only the project owner can view
    if task.project.owner != request.user:
        # behave like "not found" to avoid leaking existence
        return redirect("dashboard")

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
            return redirect("task_detail", task_id=task.id)
    else:
        form = CommentForm()

    comments = task.comments.all().order_by("-created_at")

    return render(request, "tasks/task_detail.html", {
        "task": task,
        "comments": comments,
        "form": form,
    })
