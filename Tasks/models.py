from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
# User Model

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_domain_admin = models.BooleanField(default=False)
    domain_approved = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        domain = self.email.split("@")[1]
        if not CustomUser.objects.filter(email__endswith=f'@{domain}').exists():
            # If the user is the first one for the domain, set as domain admin and approve the domain
            self.is_domain_admin = True
            self.domain_approved = True

            # Create a group for the domain and add the user to the group
            domain_group, created = Group.objects.get_or_create(name=f"{domain}_group")
            self.groups.add(domain_group)
        super().save(*args, **kwargs)
    
# ToDo Model
class Todo(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_todos')
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
# def get_or_create_domain_group(domain):
#     group, _ = Group.objects.get_or_create(name = f"{domain}_group")
#     return group
    
# @receiver(post_save, sender = CustomUser)
# def set_domain_admin(sender, instance, created, **kwargs):
#     if created:
#         domain = instance.email.split("@"[1])
#         domain_users = get_user_model().objects.filter(email__endswith = f'@{domain}')

#         if not domain_users.filter(is_domain_admin = True).exists():
#             instance.is_domain_admin = True
#             instance.save()
#         group = get_or_create_domain_group(domain)
#         instance.groups.add(group)
