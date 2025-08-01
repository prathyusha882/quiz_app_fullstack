#!/usr/bin/env python
"""
Test script to debug registration issues.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
django.setup()

from users.serializers import RegisterSerializer
from users.models import User

def test_registration():
    """Test registration with sample data."""
    
    # Test data
    test_data = {
        'username': 'testuser123',
        'email': 'test123@example.com',
        'password': 'testpass123',
        'password2': 'testpass123'
    }
    
    print("Testing registration with data:", test_data)
    
    # Test serializer validation
    serializer = RegisterSerializer(data=test_data)
    if serializer.is_valid():
        print("✅ Serializer validation passed")
        try:
            user = serializer.save()
            print(f"✅ User created successfully: {user.username}")
            # Clean up
            user.delete()
            print("✅ Test user deleted")
        except Exception as e:
            print(f"❌ Error creating user: {e}")
    else:
        print("❌ Serializer validation failed:")
        print(serializer.errors)

if __name__ == "__main__":
    test_registration() 