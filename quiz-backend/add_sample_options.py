#!/usr/bin/env python
"""
Script to add sample options to questions in the database.
Run this from the quiz-backend directory.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
django.setup()

from quizzes.models import Question, Option

def add_sample_options():
    """Add sample options to questions that don't have any."""
    
    print("All questions in database:")
    for question in Question.objects.all():
        print(f"ID: {question.id}, Text: '{question.text}', Options: {question.options.count()}")
    
    questions_updated = 0
    
    for question in Question.objects.all():
        if question.options.count() == 0:  # Only add options if question has none
            print(f"\nAdding options to question: {question.text}")
            
            # Create generic options for any question
            options_data = [
                ("Option A", True),
                ("Option B", False),
                ("Option C", False),
                ("Option D", False)
            ]
            
            # Create options
            for option_text, is_correct in options_data:
                Option.objects.create(
                    question=question,
                    text=option_text,
                    is_correct=is_correct
                )
            
            questions_updated += 1
            print(f"Added {len(options_data)} options to question {question.id}")
    
    print(f"\nUpdated {questions_updated} questions with sample options.")

if __name__ == "__main__":
    add_sample_options() 