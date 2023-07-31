from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views
from .views import UserView

urlpatterns = [
     path('',views.home,name="home"),
    #  path('list/',views.index, name="list"),
    #  path('update_task/<str:pk>/',views.update_task, name="update_task"),
     path('delete/<str:pk>/',views.tododelete, name="delete"),
     path('login/', views.login_account, name="login"),
     path('todo/',views.createtodo, name = 'todo'),
     path('dasboard/',views.dashboard,name = 'dashboard'),
     path('logout/', auth_views.LogoutView.as_view(next_page='/accounts/login'), name='logout'),
     path('profile/',login_required(UserView.as_view()),name = 'profile'),
     path('signup/', views.signup, name='signup'),
     path('assign_task/', views.assign_task, name = 'assign_task'),
     path('updatetodo/<str:pk>/',views.update_todo, name = 'updatetodo'),
]