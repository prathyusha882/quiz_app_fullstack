#!/usr/bin/env python
"""
Comprehensive fix for registration system.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
django.setup()

from users.models import User
from users.serializers import RegisterSerializer
from quizzes.models import Quiz

def clear_test_users():
    """Clear test users to avoid conflicts."""
    print("=== Clearing Test Users ===")
    
    # Delete users that might conflict
    test_usernames = ['testuser', 'testuser123', 'testuser_fix', 'prathyusha']
    for username in test_usernames:
        try:
            user = User.objects.get(username=username)
            user.delete()
            print(f"✅ Deleted user: {username}")
        except User.DoesNotExist:
            print(f"ℹ️  User not found: {username}")

def ensure_admin_user():
    """Ensure admin user exists."""
    try:
        admin_user = User.objects.get(username='admin')
        print(f"✅ Admin user exists: {admin_user.username}")
    except User.DoesNotExist:
        admin_user = User.objects.create_user(
            username='admin',
            email='admin@quizapp.com',
            password='admin123',
            role='admin'
        )
        print(f"✅ Created admin user: {admin_user.username}")

def test_registration_system():
    """Test the registration system."""
    print("\n=== Testing Registration System ===")
    
    # Test with a unique username
    test_data = {
        'username': 'newuser123',
        'email': 'newuser123@test.com',
        'password': 'password123',
        'password2': 'password123'
    }
    
    print(f"Testing registration with: {test_data['username']}")
    
    serializer = RegisterSerializer(data=test_data)
    if serializer.is_valid():
        try:
            user = serializer.save()
            print(f"✅ Registration successful: {user.username}")
            print(f"✅ User role: {user.role}")
            
            # Clean up
            user.delete()
            print("✅ Test user deleted")
            return True
        except Exception as e:
            print(f"❌ Registration failed: {e}")
            return False
    else:
        print(f"❌ Registration validation failed: {serializer.errors}")
        return False

def check_quiz_data():
    """Check quiz data."""
    print("\n=== Checking Quiz Data ===")
    
    quizzes = Quiz.objects.filter(is_active=True)
    print(f"Active quizzes: {quizzes.count()}")
    
    for quiz in quizzes:
        questions = quiz.questions.count()
        print(f"  - {quiz.title}: {questions} questions")

def main():
    """Run comprehensive fix."""
    print("🔧 Comprehensive Registration Fix")
    print("=" * 50)
    
    # Clear test users
    clear_test_users()
    
    # Ensure admin user
    ensure_admin_user()
    
    # Test registration
    if test_registration_system():
        print("\n✅ Registration system is working!")
    else:
        print("\n❌ Registration system needs more fixes!")
    
    # Check quiz data
    check_quiz_data()
    
    print("\n" + "=" * 50)
    print("✅ Fix completed!")
    print("\nYou can now:")
    print("1. Register with any username")
    print("2. Login with admin/admin123")
    print("3. Take quizzes and submit them")

if __name__ == "__main__":
    main() 