# quiz-backend/users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# Customizing the UserAdmin to show the 'role' field
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The fields to be displayed in the list view
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active', 'date_joined')
    # Fields to use for searching users
    search_fields = ('username', 'email')
    # Fields to use for filtering users
    list_filter = ('role', 'is_staff', 'is_active')

    # Add 'role' field to the fieldsets
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    # Add 'role' field to the add_fieldsets (for adding new users)
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )