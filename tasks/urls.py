from django.urls import path
from . import views

urlpatterns = [
    path("tasks/<int:task_id>", views.task_detail, name="task_detail"),
]