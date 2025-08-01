#!/usr/bin/env python
"""
Test script to verify registration works with any username.
"""

import os
import sys
import django
import random
import string

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
django.setup()

from users.models import User
from users.serializers import RegisterSerializer

def generate_random_username():
    """Generate a random username."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(8))

def test_registration_with_random_username():
    """Test registration with random username."""
    print("=== Testing Registration with Random Username ===")
    
    # Generate random username and email
    username = generate_random_username()
    email = f"{username}@test.com"
    
    test_data = {
        'username': username,
        'email': email,
        'password': 'testpass123',
        'password2': 'testpass123'
    }
    
    print(f"Testing with username: {username}")
    print(f"Testing with email: {email}")
    
    # Test serializer validation
    serializer = RegisterSerializer(data=test_data)
    if serializer.is_valid():
        print("✅ Serializer validation passed")
        try:
            user = serializer.save()
            print(f"✅ User created successfully: {user.username}")
            print(f"✅ User role: {user.role}")
            print(f"✅ User email: {user.email}")
            
            # Clean up
            user.delete()
            print("✅ Test user deleted")
            return True
        except Exception as e:
            print(f"❌ Error creating user: {e}")
            return False
    else:
        print("❌ Serializer validation failed:")
        print(serializer.errors)
        return False

def test_multiple_registrations():
    """Test multiple registrations."""
    print("\n=== Testing Multiple Registrations ===")
    
    success_count = 0
    total_tests = 5
    
    for i in range(total_tests):
        print(f"\n--- Test {i+1}/{total_tests} ---")
        if test_registration_with_random_username():
            success_count += 1
    
    print(f"\n=== Results ===")
    print(f"Successful registrations: {success_count}/{total_tests}")
    
    if success_count == total_tests:
        print("✅ All registration tests passed!")
        return True
    else:
        print("❌ Some registration tests failed!")
        return False

def check_existing_users():
    """Check existing users."""
    print("\n=== Checking Existing Users ===")
    
    users = User.objects.all()
    print(f"Total users: {users.count()}")
    
    for user in users:
        print(f"  - {user.username} ({user.email}) - Role: {user.role}")

def main():
    """Run all tests."""
    print("🧪 Testing Registration System")
    print("=" * 50)
    
    check_existing_users()
    test_multiple_registrations()
    
    print("\n" + "=" * 50)
    print("✅ Registration testing completed!")

if __name__ == "__main__":
    main() 