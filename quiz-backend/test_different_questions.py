#!/usr/bin/env python
"""
Test script to verify that different students get different questions.
Run this from the quiz-backend directory.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
django.setup()

from quizzes.models import Quiz, Question
from quizzes.views import UserQuizQuestionsView
from users.models import User
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import RefreshToken

def test_different_questions():
    """Test that different students get different questions."""
    
    # Create test users
    user1, created = User.objects.get_or_create(
        username='student1',
        defaults={'email': 'student1@test.com', 'password': 'testpass123'}
    )
    if created:
        user1.set_password('testpass123')
        user1.save()
    
    user2, created = User.objects.get_or_create(
        username='student2',
        defaults={'email': 'student2@test.com', 'password': 'testpass123'}
    )
    if created:
        user2.set_password('testpass123')
        user2.save()
    
    # Get the quiz
    quiz = Quiz.objects.filter(is_active=True).first()
    if not quiz:
        print("No active quiz found!")
        return
    
    print(f"Testing quiz: {quiz.title}")
    print(f"Total questions in quiz: {quiz.questions.count()}")
    
    # Create API request factory
    factory = APIRequestFactory()
    
    # Test for user1
    token1 = RefreshToken.for_user(user1)
    request1 = factory.get(f'/api/quizzes/{quiz.id}/questions/')
    request1.user = user1
    
    view1 = UserQuizQuestionsView.as_view()
    response1 = view1(request1, pk=quiz.id)
    
    questions1 = response1.data
    print(f"\nStudent 1 (ID: {user1.id}) gets questions:")
    print(f"Response type: {type(questions1)}")
    print(f"Response keys: {questions1.keys() if isinstance(questions1, dict) else 'Not a dict'}")
    
    # The response should be a list of questions
    if isinstance(questions1, list):
        questions_list1 = questions1
    elif isinstance(questions1, dict) and 'results' in questions1:
        questions_list1 = questions1['results']
    else:
        questions_list1 = []
    
    print(f"Questions list length: {len(questions_list1)}")
    
    for i, q in enumerate(questions_list1, 1):
        if isinstance(q, dict):
            print(f"  {i}. {q.get('text', 'No text')}")
            options = [opt.get('text', 'No text') for opt in q.get('options', [])]
            print(f"     Options: {options}")
        else:
            print(f"  {i}. {q}")
    
    # Test for user2
    token2 = RefreshToken.for_user(user2)
    request2 = factory.get(f'/api/quizzes/{quiz.id}/questions/')
    request2.user = user2
    
    view2 = UserQuizQuestionsView.as_view()
    response2 = view2(request2, pk=quiz.id)
    
    questions2 = response2.data
    print(f"\nStudent 2 (ID: {user2.id}) gets questions:")
    
    # The response should be a list of questions
    if isinstance(questions2, list):
        questions_list2 = questions2
    elif isinstance(questions2, dict) and 'results' in questions2:
        questions_list2 = questions2['results']
    else:
        questions_list2 = []
    
    print(f"Questions list length: {len(questions_list2)}")
    
    for i, q in enumerate(questions_list2, 1):
        if isinstance(q, dict):
            print(f"  {i}. {q.get('text', 'No text')}")
            options = [opt.get('text', 'No text') for opt in q.get('options', [])]
            print(f"     Options: {options}")
        else:
            print(f"  {i}. {q}")
    
    # Check if questions are different
    questions1_texts = [q.get('text', '') for q in questions_list1 if isinstance(q, dict)]
    questions2_texts = [q.get('text', '') for q in questions_list2 if isinstance(q, dict)]
    
    if questions1_texts != questions2_texts:
        print("\n✅ SUCCESS: Different students get different questions!")
    else:
        print("\n❌ FAILED: Both students got the same questions")
    
    # Check if options are shuffled
    options1 = [opt.get('text', '') for q in questions_list1 if isinstance(q, dict) for opt in q.get('options', [])]
    options2 = [opt.get('text', '') for q in questions_list2 if isinstance(q, dict) for opt in q.get('options', [])]
    
    if options1 != options2:
        print("✅ SUCCESS: Options are shuffled for different students!")
    else:
        print("❌ FAILED: Options are not shuffled")

if __name__ == "__main__":
    test_different_questions() 