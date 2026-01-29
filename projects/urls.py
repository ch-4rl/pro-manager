from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("projects/new/", views.create_project, name="create_project"),
    path("projects/<int:project_id>/", views.project_detail, name="project_detail"),
    path("projects/<int:project_id>/members/", views.project_members, name="project_members"),
    path("projects/<int:project_id>/members/<int:user_id>/remove/", views.remove_member, name="remove_member"),
    path("projects/<int:project_id>/edit/", views.edit_project, name="edit_project"),
    path("projects/<int:project_id>/delete/", views.delete_project_confirm, name="delete_project_confirm"),
    path("projects/<int:project_id>/delete/confirm/", views.delete_project, name="delete_project"),
]