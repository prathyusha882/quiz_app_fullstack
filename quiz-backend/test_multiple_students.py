#!/usr/bin/env python
"""
Test script to verify that multiple students get different questions.
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

def test_multiple_students():
    """Test that multiple students get different questions."""
    
    # Create multiple test users
    students = []
    for i in range(1, 6):  # Test 5 students
        user, created = User.objects.get_or_create(
            username=f'student{i}',
            defaults={'email': f'student{i}@test.com', 'password': 'testpass123'}
        )
        if created:
            user.set_password('testpass123')
            user.save()
        students.append(user)
    
    # Get the quiz
    quiz = Quiz.objects.filter(is_active=True).first()
    if not quiz:
        print("No active quiz found!")
        return
    
    print(f"Testing quiz: {quiz.title}")
    print(f"Total questions in quiz: {quiz.questions.count()}")
    print(f"Testing with {len(students)} students\n")
    
    # Create API request factory
    factory = APIRequestFactory()
    
    all_questions = []
    all_options = []
    
    # Test for each student
    for i, student in enumerate(students, 1):
        request = factory.get(f'/api/quizzes/{quiz.id}/questions/')
        request.user = student
        
        view = UserQuizQuestionsView.as_view()
        response = view(request, pk=quiz.id)
        
        questions = response.data
        if isinstance(questions, dict) and 'results' in questions:
            questions_list = questions['results']
        else:
            questions_list = questions if isinstance(questions, list) else []
        
        print(f"Student {i} (ID: {student.id}) gets {len(questions_list)} questions:")
        
        student_questions = []
        student_options = []
        
        for j, q in enumerate(questions_list, 1):
            if isinstance(q, dict):
                question_text = q.get('text', 'No text')
                options = [opt.get('text', 'No text') for opt in q.get('options', [])]
                
                print(f"  {j}. {question_text}")
                print(f"     Options: {options}")
                
                student_questions.append(question_text)
                student_options.extend(options)
        
        all_questions.append(student_questions)
        all_options.append(student_options)
        print()
    
    # Analyze results
    print("=== ANALYSIS ===")
    
    # Check if all students got different questions
    unique_question_sets = set()
    for questions in all_questions:
        unique_question_sets.add(tuple(sorted(questions)))
    
    if len(unique_question_sets) == len(students):
        print("✅ SUCCESS: All students got different question sets!")
    else:
        print(f"❌ FAILED: Only {len(unique_question_sets)} unique question sets for {len(students)} students")
    
    # Check for topic coverage
    print("\n=== TOPIC COVERAGE ===")
    all_topics = set()
    for questions in all_questions:
        for question in questions:
            if "JavaScript" in question or "web" in question.lower():
                all_topics.add("Web Development")
            elif "Python" in question:
                all_topics.add("Python")
            elif "React" in question:
                all_topics.add("React")
            elif "database" in question.lower() or "SQL" in question or "MongoDB" in question:
                all_topics.add("Databases")
            elif "Git" in question or "Docker" in question or "Kubernetes" in question:
                all_topics.add("DevOps")
            elif "API" in question or "HTTP" in question:
                all_topics.add("APIs")
            elif "CSS" in question or "HTML" in question:
                all_topics.add("Frontend")
            elif "Node.js" in question or "Express" in question:
                all_topics.add("Backend")
            elif "cloud" in question.lower() or "AWS" in question or "Azure" in question:
                all_topics.add("Cloud Computing")
    
    print(f"Topics covered across all students: {sorted(all_topics)}")
    
    # Check option shuffling
    print("\n=== OPTION SHUFFLING ===")
    option_variations = 0
    for i in range(len(all_options)):
        for j in range(i + 1, len(all_options)):
            if all_options[i] != all_options[j]:
                option_variations += 1
    
    total_comparisons = len(all_options) * (len(all_options) - 1) // 2
    if option_variations == total_comparisons:
        print("✅ SUCCESS: All students have different option orders!")
    else:
        print(f"⚠️  WARNING: {option_variations}/{total_comparisons} option variations")

if __name__ == "__main__":
    test_multiple_students() 