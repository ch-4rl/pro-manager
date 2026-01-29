# Pro Manager — Django Project Management App

A lightweight project management web app built with Django. Users can create projects, collaborate with members, manage tasks, and track progress with status filters.

## Features
### Authentication
- Sign up, log in, log out (Django auth)

### Projects
- Create projects
- Dashboard shows projects you own **and** projects shared with you

### Collaboration (Members)
- Project owner can add/remove members
- Members can access shared projects and tasks

### Tasks
- Create, view, edit, delete tasks
- Assign tasks to project members (or leave unassigned)
- Inline status updates from project page
- Task status updates from task detail page
- Status filters: All / To Do / Doing / Done
- “My Tasks” page shows tasks assigned to the logged-in user

### Comments
- Add comments on tasks (saved with author and timestamp)

### UI / UX
- Bootstrap styling
- Custom white / black / purple theme
- Success messages for user actions

## Tech Stack
- Python 3
- Django (6.x)
- SQLite (default database)
- Bootstrap 5 (CDN)
- HTML templates + custom CSS

## Setup (Local)
1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd pro-manager
