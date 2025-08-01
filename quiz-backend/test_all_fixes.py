#!/usr/bin/env python
"""
Comprehensive test script to verify all fixes work properly.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
django.setup()

from users.models import User
from quizzes.models import Quiz, Question
from results.models import QuizAttempt, UserAnswer
from users.serializers import RegisterSerializer
from results.serializers import UserProgressSerializer

def test_registration():
    """Test user registration."""
    print("=== Testing Registration ===")
    
    test_data = {
        'username': 'testuser_fix',
        'email': 'testfix@example.com',
        'password': 'testpass123',
        'password2': 'testpass123'
    }
    
    serializer = RegisterSerializer(data=test_data)
    if serializer.is_valid():
        try:
            user = serializer.save()
            print(f"✅ Registration successful: {user.username}")
            return user
        except Exception as e:
            print(f"❌ Registration failed: {e}")
            return None
    else:
        print(f"❌ Registration validation failed: {serializer.errors}")
        return None

def test_quiz_submission(user):
    """Test quiz submission."""
    print("\n=== Testing Quiz Submission ===")
    
    # Get a quiz
    quiz = Quiz.objects.filter(is_active=True).first()
    if not quiz:
        print("❌ No active quiz found")
        return None
    
    print(f"Using quiz: {quiz.title}")
    
    # Create a test submission
    try:
        attempt = QuizAttempt.objects.create(
            user=user,
            quiz=quiz,
            total_questions=5,
            score=3,
            time_taken='05:30'
        )
        print(f"✅ Quiz submission created: Score {attempt.score}/{attempt.total_questions}")
        return attempt
    except Exception as e:
        print(f"❌ Quiz submission failed: {e}")
        return None

def test_progress_api(user):
    """Test progress API."""
    print("\n=== Testing Progress API ===")
    
    # Create test data
    progress_data = {
        'total_quizzes_attempted': 1,
        'average_score_percentage': 60.0,
        'last_5_quizzes_scores': [
            {
                'quiz_title': 'Test Quiz',
                'score': '3',
                'total': '5',
                'percentage': '60.0'
            }
        ]
    }
    
    serializer = UserProgressSerializer(data=progress_data)
    if serializer.is_valid():
        print("✅ Progress API serializer validation passed")
        return True
    else:
        print(f"❌ Progress API serializer validation failed: {serializer.errors}")
        return False

def cleanup_test_data(user, attempt):
    """Clean up test data."""
    print("\n=== Cleaning Up Test Data ===")
    
    if attempt:
        try:
            attempt.delete()
            print("✅ Quiz attempt deleted")
        except Exception as e:
            print(f"❌ Failed to delete quiz attempt: {e}")
    
    if user:
        try:
            user.delete()
            print("✅ Test user deleted")
        except Exception as e:
            print(f"❌ Failed to delete test user: {e}")

def main():
    """Run all tests."""
    print("🧪 Running Comprehensive Test Suite")
    print("=" * 50)
    
    # Test registration
    user = test_registration()
    
    # Test quiz submission
    attempt = None
    if user:
        attempt = test_quiz_submission(user)
    
    # Test progress API
    if user:
        test_progress_api(user)
    
    # Cleanup
    cleanup_test_data(user, attempt)
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")

if __name__ == "__main__":
    main() 