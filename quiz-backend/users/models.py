# quiz-backend/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid

class User(AbstractUser):
    # Define roles as choices for consistency
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    )
    
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='student')
    
    # Email verification fields
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    email_verification_sent_at = models.DateTimeField(null=True, blank=True)
    
    # Password reset fields
    password_reset_token = models.UUIDField(null=True, blank=True)
    password_reset_sent_at = models.DateTimeField(null=True, blank=True)
    
    # Profile fields
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    
    # Account status
    is_active = models.BooleanField(default=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    account_created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)

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

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
    
    @property
    def is_student(self):
        return self.role == 'student'
    
    @property
    def is_instructor(self):
        return self.role == 'instructor'
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    def generate_email_verification_token(self):
        """Generate a new email verification token"""
        self.email_verification_token = uuid.uuid4()
        self.email_verification_sent_at = timezone.now()
        self.save()
        return self.email_verification_token
    
    def generate_password_reset_token(self):
        """Generate a new password reset token"""
        self.password_reset_token = uuid.uuid4()
        self.password_reset_sent_at = timezone.now()
        self.save()
        return self.password_reset_token
    
    def verify_email_token(self, token):
        """Verify email verification token"""
        if str(self.email_verification_token) == str(token):
            self.email_verified = True
            self.email_verification_token = None
            self.save()
            return True
        return False
    
    def verify_password_reset_token(self, token):
        """Verify password reset token"""
        if str(self.password_reset_token) == str(token):
            return True
        return False
    
    def clear_password_reset_token(self):
        """Clear password reset token after use"""
        self.password_reset_token = None
        self.password_reset_sent_at = None
        self.save()