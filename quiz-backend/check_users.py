#!/usr/bin/env python
"""
Check existing users and test registration.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
django.setup()

from users.models import User

def check_users():
    """Check existing users."""
    
    users = User.objects.all()
    print(f"Total users: {users.count()}")
    
    for user in users:
        print(f"User: {user.username}, Email: {user.email}, Role: {user.role}")

if __name__ == "__main__":
    check_users() 