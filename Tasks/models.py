

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Custom user manager to handle the user model
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set.")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_approved', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')
        if extra_fields.get('is_approved') is not True:
            raise ValueError('Superuser must have is_approved=True.')

        return self.create_user(email, password, **extra_fields)


# Custom user model inheriting from AbstractUser
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    # Use the custom user manager for the user model
    objects = CustomUserManager()

    # Remove the 'USERNAME_FIELD' since we are using 'email' as the unique identifier
    # USERNAME_FIELD = 'email'
    # Define 'REQUIRED_FIELDS' to include the 'email' field for superusers
    REQUIRED_FIELDS = ['email']

    # Remove 'username' field as it is inherited from AbstractUser
    # Keep other fields like 'first_name', 'last_name', 'date_joined', etc. from AbstractUser
    # Add the new fields 'is_admin' and 'is_approved'
    # Remove 'full_name' field as per the request


class TodoItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_todos', null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
