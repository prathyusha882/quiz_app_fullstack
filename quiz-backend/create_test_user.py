#!/usr/bin/env python
"""
Script to create a test user for testing.
Run this from the quiz-backend directory.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
django.setup()

from django.contrib.auth import get_user_model

def create_test_user():
    """Create a test user for testing."""
    
    User = get_user_model()
    
    # Check if test user already exists
    if User.objects.filter(username='testuser').exists():
        print("Test user already exists!")
        return
    
    # Create test user
    test_user = User.objects.create_user(
        username='testuser',
        email='test@quizapp.com',
        password='test123',
        first_name='Test',
        last_name='User'
    )
    
    print(f"✅ Created test user:")
    print(f"   Username: testuser")
    print(f"   Password: test123")
    print(f"   Email: test@quizapp.com")
    print(f"   Name: {test_user.first_name} {test_user.last_name}")

if __name__ == "__main__":
    create_test_user() 