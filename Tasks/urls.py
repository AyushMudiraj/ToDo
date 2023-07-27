from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home_view, name='home'),
    path('register/',views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name = 'dashboard'),
    path('login/',views.login_view, name='login'),
    path('approve/<int:user_id>/', views.domain_approval_view, name='approve_user'),
    path('logout/', views.logout_view, name='logout'),
    path('mark_complete/<int:todo_id>', views.mark_complete_view, name = 'mark_complete'),
]