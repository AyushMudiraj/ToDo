# from django import forms
# from django.forms import ModelForm, Form
# from django.contrib.auth.forms import UserCreationForm
# from .models import *

# class RegistrationForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ('email', 'password1','password2')

# class LoginForm(forms.Form):
#     # email = forms.EmailField()
#     password = forms.CharField(label= 'Password', widget=forms.PasswordInput)
#     class Meta:
#         model = CustomUser
#         fields = ('email', 'password')
    
# class UserApprovalForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ('domain_approved',)

# class TodoForm(forms.ModelForm):
#     class Meta:
#         model = TodoItem
#         fields = ['title', 'description', 'assigned_to']
