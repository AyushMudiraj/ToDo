from django.db import models
from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin, Group, Permission
# from django.contrib.auth import get_user_model
from django.utils import timezone


# Create your models here.

# class User(models.Models):
    


# Create your models here.
class UserManager(BaseUserManager):
    def _create_user(self,email,password,is_staff,is_superuser,is_admin,domain,**extra_fields):
        if not email:
            raise ValueError("Users must have an email address\n")
        email=self.normalize_email(email)
        now=timezone.now()
        user=self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            last_login=now,
            date_joined=now,
            is_admin=is_admin,
            domain=domain,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password, **extra_fields):
        return self._create_user(email,password,True, False, False,**extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        user=self._create_user(email,password, True, True, True,**extra_fields)
        return user
    
    

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    domain=models.CharField(max_length=100, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    
    # Add the related_name attribute to differentiate reverse accessor names
    groups = models.ManyToManyField(Group, related_name='user')
    user_permissions = models.ManyToManyField(Permission, related_name='user')
    
    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    title= models.CharField(max_length=200)
    description = models.CharField(max_length = 1000, null = True, blank = True)
    complete = models.BooleanField(default=False)
    created= models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title, self.description
    