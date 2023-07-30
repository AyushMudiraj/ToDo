from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.views.generic.detail import DetailView
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request,'Tasks/base.html')

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
    # form = TaskForm()
    user = request.user
    context = {"tasks":tasks, "user": user}
    
    
    if user.is_authenticated:
        return render(request,"Tasks/profile.html", context)
    
    destination = get_redirect_if_exists(request)
    
    
    if request.POST:
        form= AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            
            if user:
                fresh_context = {"tasks":tasks,"user":user}
                login(request,user)
                # destination= get_redirect_if_exists(request)
                if destination:
                    return redirect(destination)
                return render(request,'Tasks/profile.html',fresh_context)
        else:
            context['login_form']=form
    return render(request,'Tasks/login.html',context)


def get_redirect_if_exists(request):
    redirect=None
    if request.GET:
        if request.GET.get("next"):
            redirect=str(request.GET.get("next"))
    return redirect

# def index(request):
#     # import ipdb;ipdb.set_trace()
#     tasks = Task.objects.all()
    
#     form=TaskForm()
    
#     if request.method == 'POST':
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             form.save()
#         return redirect('list')
#     else:
#         user=request.user
#         context={'tasks':tasks,'user':user,'form':form}
#         return render(request,'Tasks/profile.html',context)
#     # context = {'tasks':tasks, 'form':form}
#     # return render(request,'tasks/list.html', context)
    
def assign_domain_admin(user):
    if not User.objects.filter(domain=user.domain, is_admin=True).exists():
        user.is_admin = True
        user.save()

class UserView(DetailView):
    template_name = 'Tasks/profile.html'

    def get_object(self):
        return self.request.user


@login_required
def createtodo(request):
    if request.method == 'GET':
        user = request.user
        mytodo = Task.objects.all()
        context = {
              "todos":mytodo,
              "form":TaskForm(),
              "user":user
		}
        return render(request, "Tasks/todo.html", context)
    else:
        try:
            form = TaskForm(request.POST)
            if form.is_valid():
                  newtodo = form.save()
                  newtodo.user = request.user
                  newtodo.save()
                #   return redirect('www.facebook.com')

            # newtodo = form.save(commit=False)
            # newtodo.user = request.user
            # newtodo.save()
            return redirect('todo')
        except ValueError:
            return render(request, "Tasks/todo.html", {'form':TaskForm(), 'error':'Wrong data provided. Try again.'})
        


# def update_task(request, pk):
#     task= Task.objects.get(id=pk)
#     print(pk)
#     form = TaskForm(instance=task)
    
#     if request.method == 'POST':
#         form = TaskForm(request.POST, instance=task)
#         print("fgvhgvfcghjuhgbvgh")
#         if form.is_valid():
#             form.save()
#             return redirect('list')
    
#     context = {'form':form}
 
#     return render(request, 'Tasks/add_todo.html', context)


def deletetodo(request, pk):
    item=Task.objects.get(id=pk)
    
    if request.method == 'POST':
        item.delete()
        return redirect('todo')
        
    
    context ={'item':item}
    return render(request,'Tasks/delete.html', context)


def dashboard(request):
     users = User.objects.all()
     user = request.user
     print(user)
     mytodo = Task.objects.all()
     context = {
          "users":users,
          "mytodo":mytodo,
          "curr":user
     }
     return render(request,'Tasks/dashboard.html',context)
# def login(request):

def assign_task(request,pk):
     if request.method == 'POST':
          users = User.objects.all()
          context = {
               "all_user":users,
              "user":User.objects.get(id=pk),
              "form":TaskForm(),
              "curr_user" :request.user,
              }
        #   print(request.user)
          assign_to = User.objects.get(id=pk)
        #   print(assign_to)
        #   print(pk)
          print(request.user.id)
          form = TaskForm(request.POST)
          if form.is_valid():
            newtodo = form.save()
            newtodo.user = assign_to
            newtodo.save()
          return render(request, "Tasks/dashboard.html",context)
     context = {
              "user":request.user,
              "form":TaskForm(),
              "assign_to":User.objects.get(id=pk),
              }
     
     return render(request,"Tasks/assign.html",context)
 
def update_todo(request, pk):
	todo = Task.objects.get(id=pk)

	form = TaskForm(instance=todo)

	if request.method == 'POST':
		form = TaskForm(request.POST, instance=todo)
		if form.is_valid():
			form.save()
			return redirect('todo')

	context = {'form':form}

	return render(request, "Tasks/update.html", context)

     





