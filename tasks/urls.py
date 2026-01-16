from django.urls import path
from . import views

urlpatterns = [
    path("tasks/<int:task_id>", views.task_detail, name="task_detail"),
    path("tasks/<int:task_id>/edit/", views.edit_task, name="edit_task"),
    path("tasks/<int:task_id>/status/", views.update_task_status, name="update_task_status"),
    path("tasks/<int:task_id>/delete/", views.delete_task_confirm, name="delete_task_confirm"),
    path("tasks/<int:task_id>/delete/confirm/", views.delete_task, name="delete_task"), 
]