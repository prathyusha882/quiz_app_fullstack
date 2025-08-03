#!/usr/bin/env python
"""
Test script for new features:
- Email verification
- Password reset
- Certificate generation
- Async tasks
- Analytics
"""

import os
import sys
import django
from datetime import timedelta

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from users.models import User
from quizzes.models import Quiz, Question, Option, Tag
from results.models import QuizAttempt, UserAnswer, Certificate, QuizAnalytics, Leaderboard
from users.services import EmailService
from results.services import CertificateService
from users.tasks import send_verification_email_task, send_password_reset_email_task
from results.tasks import process_quiz_completion, generate_certificate_task

def test_email_verification():
    """Test email verification functionality"""
    print("🧪 Testing Email Verification...")
    
    # Create a test user
    user, created = User.objects.get_or_create(
        username='test_verification',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'student'
        }
    )
    
    if created:
        user.set_password('test123')
        user.save()
        print(f"✅ Created test user: {user.username}")
    
    # Test email verification
    try:
        success = EmailService.send_verification_email(user)
        if success:
            print("✅ Email verification email sent successfully")
        else:
            print("❌ Failed to send verification email")
    except Exception as e:
        print(f"❌ Error sending verification email: {e}")
    
    # Test async task
    try:
        result = send_verification_email_task.delay(user.id)
        print(f"✅ Async email verification task queued: {result.id}")
    except Exception as e:
        print(f"❌ Error queuing async task: {e}")

def test_password_reset():
    """Test password reset functionality"""
    print("\n🧪 Testing Password Reset...")
    
    # Get or create test user
    user, created = User.objects.get_or_create(
        username='test_reset',
        defaults={
            'email': 'reset@example.com',
            'first_name': 'Reset',
            'last_name': 'User',
            'role': 'student'
        }
    )
    
    if created:
        user.set_password('test123')
        user.save()
        print(f"✅ Created test user: {user.username}")
    
    # Test password reset
    try:
        success = EmailService.send_password_reset_email(user)
        if success:
            print("✅ Password reset email sent successfully")
        else:
            print("❌ Failed to send password reset email")
    except Exception as e:
        print(f"❌ Error sending password reset email: {e}")
    
    # Test async task
    try:
        result = send_password_reset_email_task.delay(user.id)
        print(f"✅ Async password reset task queued: {result.id}")
    except Exception as e:
        print(f"❌ Error queuing async task: {e}")

def test_certificate_generation():
    """Test certificate generation"""
    print("\n🧪 Testing Certificate Generation...")
    
    # Get or create test user
    user, created = User.objects.get_or_create(
        username='test_cert',
        defaults={
            'email': 'cert@example.com',
            'first_name': 'Certificate',
            'last_name': 'User',
            'role': 'student'
        }
    )
    
    if created:
        user.set_password('test123')
        user.save()
        print(f"✅ Created test user: {user.username}")
    
    # Get or create test quiz
    quiz, created = Quiz.objects.get_or_create(
        title='Test Certificate Quiz',
        defaults={
            'description': 'A test quiz for certificate generation',
            'difficulty': 'easy',
            'duration': 30,
            'time_limit': 30,
            'passing_score': 70,
            'created_by': user,
            'status': 'published'
        }
    )
    
    if created:
        print(f"✅ Created test quiz: {quiz.title}")
    
    # Get or create test attempt
    attempt, created = QuizAttempt.objects.get_or_create(
        user=user,
        quiz=quiz,
        defaults={
            'score': 8,
            'total_questions': 10,
            'correct_answers': 8,
            'incorrect_answers': 2,
            'percentage_score': 80.0,
            'passed': True,
            'is_completed': True,
            'is_submitted': True,
            'submitted_at': timezone.now(),
            'time_taken': timedelta(minutes=25)
        }
    )
    
    if created:
        print(f"✅ Created test attempt: Score {attempt.score}/{attempt.total_questions}")
    
    # Test certificate generation
    try:
        certificate = CertificateService.create_certificate_for_attempt(attempt)
        if certificate:
            print(f"✅ Certificate generated successfully: {certificate.certificate_number}")
        else:
            print("❌ Failed to generate certificate")
    except Exception as e:
        print(f"❌ Error generating certificate: {e}")
    
    # Test async certificate generation
    try:
        result = generate_certificate_task.delay(attempt.id)
        print(f"✅ Async certificate generation task queued: {result.id}")
    except Exception as e:
        print(f"❌ Error queuing async certificate task: {e}")

def test_analytics():
    """Test analytics functionality"""
    print("\n🧪 Testing Analytics...")
    
    # Get or create analytics for a quiz
    quiz = Quiz.objects.first()
    if quiz:
        analytics, created = QuizAnalytics.objects.get_or_create(quiz=quiz)
        if created:
            print(f"✅ Created analytics for quiz: {quiz.title}")
        
        # Update analytics
        try:
            analytics.update_analytics()
            print(f"✅ Analytics updated: {analytics.total_attempts} attempts, {analytics.average_score}% avg score")
        except Exception as e:
            print(f"❌ Error updating analytics: {e}")
    else:
        print("❌ No quizzes found for analytics test")

def test_leaderboard():
    """Test leaderboard functionality"""
    print("\n🧪 Testing Leaderboard...")
    
    quiz = Quiz.objects.first()
    if quiz:
        # Clear existing leaderboard
        Leaderboard.objects.filter(quiz=quiz).delete()
        
        # Get completed attempts
        attempts = QuizAttempt.objects.filter(
            quiz=quiz,
            is_completed=True,
            is_valid=True
        ).order_by('-percentage_score', 'time_taken')
        
        # Create leaderboard entries
        for rank, attempt in enumerate(attempts, 1):
            Leaderboard.objects.create(
                quiz=quiz,
                user=attempt.user,
                attempt=attempt,
                score=attempt.score,
                percentage_score=attempt.percentage_score,
                time_taken=attempt.time_taken,
                rank=rank
            )
        
        print(f"✅ Leaderboard updated: {attempts.count()} entries")
    else:
        print("❌ No quizzes found for leaderboard test")

def test_async_processing():
    """Test async task processing"""
    print("\n🧪 Testing Async Processing...")
    
    attempt = QuizAttempt.objects.filter(is_completed=True).first()
    if attempt:
        try:
            result = process_quiz_completion.delay(attempt.id)
            print(f"✅ Async quiz completion processing queued: {result.id}")
        except Exception as e:
            print(f"❌ Error queuing async processing: {e}")
    else:
        print("❌ No completed attempts found for async processing test")

def main():
    """Run all tests"""
    print("🚀 Testing New Features")
    print("=" * 50)
    
    test_email_verification()
    test_password_reset()
    test_certificate_generation()
    test_analytics()
    test_leaderboard()
    test_async_processing()
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")
    print("\nTo test email functionality:")
    print("1. Set up email configuration in .env")
    print("2. Start Celery worker: celery -A quiz_project worker --loglevel=info")
    print("3. Check email logs for verification and reset emails")

if __name__ == '__main__':
    main() 