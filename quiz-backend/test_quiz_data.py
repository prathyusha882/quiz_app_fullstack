#!/usr/bin/env python
"""
Test script to check quiz data.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
django.setup()

from quizzes.models import Quiz

def check_quiz_data():
    """Check if quiz data exists."""
    
    active_quizzes = Quiz.objects.filter(is_active=True)
    print(f"Active quizzes: {active_quizzes.count()}")
    
    for quiz in active_quizzes:
        print(f"Quiz ID: {quiz.id}, Title: {quiz.title}")
        print(f"Questions: {quiz.questions.count()}")
        print(f"Description: {quiz.description}")
        print("---")

if __name__ == "__main__":
    check_quiz_data() 