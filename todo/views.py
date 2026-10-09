from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Task

# Login View
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'todo/login.html', {'form': form})

# Registration View
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'todo/register.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# Main Dashboard (Search & Filter ke sath)
@login_required
def index(request):
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('filter', 'all')

    tasks = Task.objects.filter(user=request.user)

    # Search Logic
    if search_query:
        tasks = tasks.filter(title__icontains=search_query)

    # Filter Logic
    if status_filter == 'completed':
        tasks = tasks.filter(completed=True)
    elif status_filter == 'pending':
        tasks = tasks.filter(completed=False)

    if request.method == "POST":
        title = request.POST.get('title')
        if title:
            Task.objects.create(user=request.user, title=title)
            return redirect('index')

    context = {
        'tasks': tasks,
        'search_query': search_query,
        'status_filter': status_filter
    }
    return render(request, 'todo/index.html', context)

# Task Toggle (Check/Uncheck)
@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('index')

# Edit Task
@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        title = request.POST.get('title')
        if title:
            task.title = title
            task.save()
            return redirect('index')
    return render(request, 'todo/edit_task.html', {'task': task})

# Delete Task
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('index')