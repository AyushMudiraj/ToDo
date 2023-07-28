# todo/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import TodoItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, login, authenticate, get_user
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseForbidden
from django.contrib.auth import logout as django_logout

CustomUser = get_user_model()

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # You can add more fields here if required

    # Check if the email is already registered
        if get_user_model().objects.filter(email=email).exists():
            # Handle the case when the email is already registered
            return render(request, 'Tasks/register.html', {'error_message': 'Email is already registered.'})

        # Create a new user instance
        user = get_user_model().objects.create_user(email=email, password=password, is_approved=False)

        # Redirect to the login page after successful registration
        return redirect('login')
    return render(request, 'Tasks/register.html')

def custom_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_approved:
                login(request, user)
                return redirect('dashboard', {'user' : user})
            else:
                return HttpResponseForbidden("Your account has not been approved yet. Please wait for the domain admin to approve your registration.")
    else:
        form = AuthenticationForm(request)
        user = get_user(request)
    return render(request, 'Tasks/login.html', {'form': form, 'user':user})


@login_required
def todo_list(request):
    todos = TodoItem.objects.filter(user=request.user)

    # Filter todos based on the user's domain
    todos = todos.filter(user__email__endswith=request.user.email.split('@')[1])

    return render(request, 'Tasks/dashboard.html', {'todos': todos})

@login_required
def add_todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        assigned_to_id = request.POST.get('assigned_to')  # Get assigned_to user id from the form

        assigned_to = get_object_or_404(get_user_model(), id=assigned_to_id) if assigned_to_id else None

        TodoItem.objects.create(title=title, description=description, user=request.user, assigned_to=assigned_to)
        return redirect('dashboard')
    
    users = get_user_model().objects.filter(email__endswith=request.user.email.split('@')[1])  # Filter users within the same domain
    return render(request, 'Tasks/add_todo.html', {'users': users})

@login_required
def approve_user(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    
    # Check if the current user is the domain admin
    domain = request.user.email.split('@')[1]
    if not request.user.is_admin or not user.email.endswith(domain):
        return HttpResponseForbidden("You don't have permission to approve this user.")

    # Approve the user
    user.is_approved = True
    user.save()
    
    return redirect('group_todo_list')

@login_required
def group_todo_list(request):
    User = get_user_model()
    domain_groups = {}
    for user in User.objects.all():
        domain = user.email.split('@')[1]
        if domain in domain_groups:
            domain_groups[domain].append(user)
        else:
            domain_groups[domain] = [user]
    return render(request, 'Tasks/group_todo_list.html', {'domain_groups': domain_groups})

@login_required
def mark_todo_complete(request, todo_id):
    todo = get_object_or_404(TodoItem, id=todo_id)

    # Check if the user is assigned to the todo or if the user is the creator of the todo
    if todo.assigned_to == request.user or todo.user == request.user:
        todo.is_completed = True
        todo.save()

    return redirect('dashboard')

@login_required
def delete_todo(request, todo_id):
    todo = get_object_or_404(TodoItem, id=todo_id)

    # Check if the user is the creator of the todo
    if todo.user == request.user:
        todo.delete()

    return redirect('dashboard')
@login_required
def logout(request):
    django_logout(request)
    return redirect('login')