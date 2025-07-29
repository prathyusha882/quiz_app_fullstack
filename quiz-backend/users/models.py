# quiz-backend/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Define roles as choices for consistency
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    # Add related_name to avoid conflicts if you also have other models linking to User
    # Default related_name for groups/user_permissions might conflict if using multiple custom user models.
    # If this is your ONLY custom user model, these are not strictly necessary but good practice.
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=('groups'),
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="user_set_custom", # Changed related_name
        related_query_name="user_custom",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name="user_set_custom", # Changed related_name
        related_query_name="user_custom",
    )

    def __str__(self):
        return self.username