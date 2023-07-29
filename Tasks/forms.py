from typing import Any, Dict
from django import forms
from django.forms import ModelForm
from requests import request

from .models import *

from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse

class TaskForm(forms.ModelForm):
    title= forms.CharField(widget= forms.TextInput(attrs={'placeholder':'Add new task...'}))
    class Meta:
        model = Task
        fields = '__all__'
        
        

 
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)
        
        
class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label="Password",widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('email','password')
        
    # def save(self):
    #     email = self.cleaned_data['email']
    #     password = self.cleaned_data['password']
    #     user = authenticate(email=email, password=password)
    #     if user:
    #         login(request,user)
        
        
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid Login")
                
        
        