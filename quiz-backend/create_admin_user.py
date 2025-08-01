#!/usr/bin/env python
"""
Script to create an admin user for testing.
Run this from the quiz-backend directory.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

def create_admin_user():
    """Create an admin user for testing."""
    
    User = get_user_model()
    
    # Check if admin user already exists
    if User.objects.filter(username='admin').exists():
        print("Admin user already exists!")
        return
    
    # Create admin user
    admin_user = User.objects.create_user(
        username='admin',
        email='admin@quizapp.com',
        password='admin123',
        is_staff=True,
        is_superuser=True
    )
    
    print(f"✅ Created admin user:")
    print(f"   Username: admin")
    print(f"   Password: admin123")
    print(f"   Email: admin@quizapp.com")
    print(f"   Is Staff: {admin_user.is_staff}")
    print(f"   Is Superuser: {admin_user.is_superuser}")

if __name__ == "__main__":
    create_admin_user() 