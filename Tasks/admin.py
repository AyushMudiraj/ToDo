from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.
# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     list_display = ('email', 'is_staff', 'is_domain_admin', 'domain_approved')
#     list_filter = ('is_staff', 'is_domain_admin', 'domain_approved')
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Permissions', {'fields': ('is_staff', 'is_domain_admin', 'domain_approved')}),
#         ('Important dates', {'fields': ('last_login',)}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2'),
#         }),
#     )
#     ordering = ('email',)
#     search_fields = ('email',)

# Custom admin class for the custom user model
class CustomUserAdmin(UserAdmin):
    # Remove 'ordering' and 'list_display' as they are not required for the custom admin class
    list_filter = ['is_active', 'is_admin', 'is_approved']
    search_fields = ['email']

    # Override the 'fieldsets' to include the relevant fields in the 'add' and 'change' forms
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'is_approved')}),
        # Keep other relevant fields here as per your requirements
    )

    # Override the 'add_fieldsets' to include the relevant fields in the 'add' form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_admin', 'is_approved'),
        }),
    )
    
admin.site.register(CustomUser, UserAdmin)
admin.site.register(TodoItem)

