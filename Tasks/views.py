from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import CustomUser, Todo

# Create your views here.
def home_view(request):
    return render(request, 'Tasks/home.html')


def register_view(request):
    if request.method == 'POST':
        print("hiiiiii")
        form = RegistrationForm(request.POST)
        print("hell")
        if form.is_valid():
            print('ooooo')
            form.save()
            return redirect('login')
    else:
        print("noooo")
        form = RegistrationForm()
    print("Wayyyy")
    return render(request, 'Tasks/register.html', {'form': form})

def login_view(request):
    
    if request.method == 'POST':
        
        form = LoginForm(request.POST)
        # print("Helo Post")
        if form.is_valid():
            print("Helo Post00000000000000000000")
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            # print("Helo Post1237")
            if user is not None:
                # print("Helo Post")
                login(request, user)
                return redirect('dashboard')
    else:
        form = LoginForm()
        print("Helo Not Post")
    print("return hello")
    return render(request, 'Tasks/login.html', {'form': form})

def logout_view(request):
     logout(request)
     return redirect('login')

@login_required
def dashboard_view(request):
    is_domain_admin = request.user.is_authenticated and request.user.is_domain_admin

    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)

            if is_domain_admin:
                todo.save()
            else:
                todo.assigned_to = request.user
                todo.save()

            return redirect('dashboard')
    else:
        form = TodoForm()
        return render(request, 'Tasks/dashboard_user.html')
    if is_domain_admin:
        domain = request.user.email.split("@")[1]
        domain_users = CustomUser.objects.filter(email__endswith=f'@{domain}', domain_approved=True)
        todos = Todo.objects.filter(assigned_to__in=domain_users)
        return render(request, 'Tasks/dashboard_admin.html', {'form': form, 'domain_users': domain_users, 'todos': todos})
    else:
        todos = Todo.objects.filter(assigned_to=request.user)
        return render(request, 'Tasks/dashboard_user.html', {'form': form, 'todos': todos})

def mark_complete_view(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, assigned_to=request.user)
    todo.completed = True
    todo.save()
    return redirect('dashboard')


def domain_approval_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if not request.user.is_authenticated or not request.user.is_domain_admin:
        return redirect('login')

    if request.method == 'POST':
        user.domain_approved = True
        user.save()
        return redirect('dashboard')

    return render(request, 'Tasks/domain_approval.html', {'user': user})

@login_required
def approve_user_view(request, user_id):
    # Check if the user is a domain admin
    is_domain_admin = request.user.is_authenticated and request.user.is_domain_admin

    if is_domain_admin:
        user = get_object_or_404(CustomUser, id=user_id, domain_approved=False)
        if request.method == 'POST':
            form = UserApprovalForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
        else:
            form = UserApprovalForm(instance=user)

        return render(request, 'Tasks/domain_approval.html', {'form': form, 'user': user})
    else:
        return redirect('dashboard')