#!/usr/bin/env python
"""
Debug registration with exact data being sent.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
django.setup()

from users.serializers import RegisterSerializer
from users.models import User

def debug_registration():
    """Debug registration with sample data."""
    
    # Test data that might be sent from frontend
    test_cases = [
        {
            'username': 'testuser123',
            'email': 'test123@example.com',
            'password': 'testpass123',
            'password2': 'testpass123'
        },
        {
            'username': 'prathyusha',
            'email': 'prathyusha@example.com',
            'password': 'password123',
            'password2': 'password123'
        }
    ]
    
    for i, test_data in enumerate(test_cases, 1):
        print(f"\n=== Test Case {i} ===")
        print(f"Data: {test_data}")
        
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
    debug_registration() 