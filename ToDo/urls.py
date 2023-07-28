"""ToDo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# project_name/urls.py

from django.contrib import admin
from django.urls import path, include
from Tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Tasks.urls')),
     # Custom authentication URLs
    
    path('accounts/register/', views.register, name='register'),
    path('accounts/login/', views.custom_login_view, name='login'),
    path('accounts/logout/', views.logout, name='logout'),
    path('accounts/dashboard/', views.todo_list, name='dashboard'),
    path('accounts/add/', views.add_todo, name='add_todo'),
    path('accounts/group/', views.group_todo_list, name='group_todo_list'),
    path('accounts/approve/<int:user_id>/', views.approve_user, name='approve_user'),
    path('accounts/complete/<int:todo_id>/', views.mark_todo_complete, name='mark_todo_complete'),
    path('accounts/delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
]

