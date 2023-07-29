from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import *
from .forms import *
from django.contrib.auth import login, authenticate, logout

from django.views.generic.detail import DetailView


# Create your views here.
def home(request):
    return render(request,'Tasks/base.html')

def index(request):
    # import ipdb;ipdb.set_trace()
    tasks = Task.objects.all()
    
    form=TaskForm()
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('list')
    else:
        user=request.user
        context={'tasks':tasks,'user':user,'form':TaskForm()}
        return render(request,'tasks/dashboard.html',context)
    # context = {'tasks':tasks, 'form':form}
    # return render(request,'tasks/list.html', context)

def update_task(request, pk):
    task= Task.objects.get(id=pk)
    print(pk)
    form = TaskForm(instance=task)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        print("fgvhgvfcghjuhgbvgh")
        if form.is_valid():
            form.save()
            return redirect('list')
    
    context = {'form':form}
 
    return render(request, 'Tasks/add_todo.html', context)


def deleteTask(request, pk):
    item=Task.objects.get(id=pk)
    
    if request.method == 'POST':
        item.delete()
        return redirect('list')
        
    
    context ={'item':item}
    return render(request,'Tasks/dashboard.html', context)

# def login(request):


class UserView(DetailView):
    template_name = 'Tasks/profile.html'

    def get_object(self):
        return self.request.user


def assign_domain_admin(user):
    if not User.objects.filter(domain=user.domain, is_admin=True).exists():
        user.is_admin = True
        user.save()

def signup(request):
    # import ipdb;ipdb.set_trace()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            
            dom=form.cleaned_data.get('email')
            res = str(dom[dom.index('@') + 1 : ])
            user.domain=res
            user.save()
            user = authenticate(request, email=user.email, password=raw_password)
            if user is not None:
                login(request, user)
            else:
                print("user is not authenticated")
                
            assign_domain_admin(user)
            print(user.domain)
            print(user.is_admin)
            if user.is_admin == False:
                user.is_active = False
            user.save()
            return redirect('profile')
    else:
        form = SignUpForm()
    return render(request, 'Tasks/register.html', {'form': form})    
def logoutView(request):
    logout(request)
    return redirect("login")

def loginView(request):
    tasks = Task.objects.all()
    form = TaskForm()
    context = {"tasks":tasks, "form":form}
    user = request.user
    
    # if user.is_authenticated():
    #     return redirect("tasks:list")
    
    if request.POST:
        form= AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request,user)
                destination= get_redirect_if_exists(request)
                if destination:
                    return redirect(destination)
                return render(request,"Tasks/dashboard.html",context)
        else:
            context['login_form']=form
    return render(request,'Tasks/login.html',context)


def get_redirect_if_exists(request):
    redirect=None
    if request.GET:
        if request.GET.get("next"):
            redirect=str(request.GET.get("next"))
    return redirect