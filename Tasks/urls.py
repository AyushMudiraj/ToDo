# todo/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.custom_login_view,  name='login'),
    path('logout/', views.logout, name = 'logout'),
    path('dashboard/', views.todo_list, name='dashboard'),
    path('add/', views.add_todo, name='add_todo'),
    path('group/', views.group_todo_list, name='group_todo_list'),
    path('approve/<int:user_id>/', views.approve_user, name='approve_user'),
    path('complete/<int:todo_id>/', views.mark_todo_complete, name='mark_todo_complete'),
    path('delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    
    # path('accounts/register/', views.register, name='register'),
    # path('accounts/login/', views.custom_login_view, name='login'),
    # path('accounts/logout/', views.logout, name='logout'),
    # path('accounts/dashboard/', views.todo_list, name='dashboard'),
    # path('accounts/add/', views.add_todo, name='add_todo'),
    # path('accounts/group/', views.group_todo_list, name='group_todo_list'),
    # path('accounts/approve/<int:user_id>/', views.approve_user, name='approve_user'),
    # path('accounts/complete/<int:todo_id>/', views.mark_todo_complete, name='mark_todo_complete'),
    # path('accounts/delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    
]
