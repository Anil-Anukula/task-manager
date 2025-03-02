from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task, List, Tag
from .forms import TaskForm
from datetime import date
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm



def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after registration
            return redirect("home")  # Redirect to home page after successful signup
    else:
        form = UserCreationForm()

    return render(request, "tasks/register.html", {"form": form})

def custom_login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect if already logged in

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'tasks/login.html', {'form': form})
@login_required
def custom_logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page


@login_required
def home(request):
    """Home page displaying lists and tasks with filtering"""
    today = date.today()

    if not request.user.is_authenticated:
        return render(request, 'tasks/home.html')  # For unauthenticated users
    
    lists = List.objects.filter(user=request.user)

    # Fetch the filter parameter from the URL
    filter_option = request.GET.get("filter", "all")

    # Base QuerySet
    tasks = Task.objects.filter(user=request.user, is_deleted=False).order_by('-created_at')

    # Apply filtering
    if filter_option == "completed":
        tasks = tasks.filter(is_completed=True)
    elif filter_option == "pending":
        tasks = tasks.filter(is_completed=False)
    elif filter_option == "overdue":
        tasks = tasks.filter(due_date__lt=today, is_completed=False)
    elif filter_option == "today":
        tasks = tasks.filter(due_date=today, is_completed=False)

    completed_tasks = Task.objects.filter(user=request.user, is_completed=True).count()
    pending_tasks = Task.objects.filter(user=request.user, is_completed=False, is_deleted=False).count()

    context = {
        'lists': lists,
        'tasks': tasks,
        'today': today,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'filter_option': filter_option,  # Pass selected filter to template
    }
    return render(request, 'tasks/home.html', context)




@login_required
def task_create(request):
    """Create a new task."""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            form.save_m2m()  # Save many-to-many fields (tags)
            return redirect('home')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_update(request, task_id):
    """Update an existing task."""
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_delete(request, task_id):
    """Soft-delete a task by setting is_deleted=True."""
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('home')



@login_required
def toggle_task_completion(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.is_completed = not task.is_completed
    task.save()
    return redirect('home')