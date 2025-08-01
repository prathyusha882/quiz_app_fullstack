#!/usr/bin/env python
"""
Quick fix script to ensure everything is working properly.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
django.setup()

from users.models import User
from quizzes.models import Quiz, Question, Option

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

def ensure_test_user():
    """Ensure test user exists."""
    try:
        test_user = User.objects.get(username='testuser')
        print(f"✅ Test user exists: {test_user.username}")
    except User.DoesNotExist:
        test_user = User.objects.create_user(
            username='testuser',
            email='test@quizapp.com',
            password='test123',
            role='student'
        )
        print(f"✅ Created test user: {test_user.username}")

def check_quiz_data():
    """Check quiz data."""
    quizzes = Quiz.objects.filter(is_active=True)
    print(f"✅ Active quizzes: {quizzes.count()}")
    
    for quiz in quizzes:
        questions = quiz.questions.count()
        print(f"  - {quiz.title}: {questions} questions")

def main():
    """Run quick fixes."""
    print("🔧 Running Quick Fixes")
    print("=" * 30)
    
    ensure_admin_user()
    ensure_test_user()
    check_quiz_data()
    
    print("\n" + "=" * 30)
    print("✅ Quick fixes completed!")
    print("\nYou can now:")
    print("1. Login with admin/admin123")
    print("2. Login with testuser/test123")
    print("3. Take quizzes and submit them")
    print("4. Register new users")

if __name__ == "__main__":
    main() 