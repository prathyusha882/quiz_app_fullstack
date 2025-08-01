#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
django.setup()

from quizzes.models import Quiz, Question, Option

def update_questions():
    print("Updating questions with better programming content...")
    
    # Get the Demo Quiz
    demo_quiz = Quiz.objects.get(id=1)
    print(f"Updating questions for: {demo_quiz.title}")
    
    # Clear existing questions for this quiz
    Question.objects.filter(quiz=demo_quiz).delete()
    print("Cleared existing questions")
    
    # Define new questions with proper options
    new_questions = [
        {
            'text': 'Which programming language is known as the "language of the web"?',
            'options': [
                {'text': 'JavaScript', 'is_correct': True},
                {'text': 'Python', 'is_correct': False},
                {'text': 'Java', 'is_correct': False},
                {'text': 'C++', 'is_correct': False}
            ]
        },
        {
            'text': 'What does HTML stand for?',
            'options': [
                {'text': 'HyperText Markup Language', 'is_correct': True},
                {'text': 'High Tech Modern Language', 'is_correct': False},
                {'text': 'Home Tool Markup Language', 'is_correct': False},
                {'text': 'Hyperlink and Text Markup Language', 'is_correct': False}
            ]
        },
        {
            'text': 'Which of the following is a JavaScript framework?',
            'options': [
                {'text': 'React', 'is_correct': True},
                {'text': 'Django', 'is_correct': False},
                {'text': 'Flask', 'is_correct': False},
                {'text': 'Express', 'is_correct': False}
            ]
        },
        {
            'text': 'What is the purpose of CSS in web development?',
            'options': [
                {'text': 'To style and layout web pages', 'is_correct': True},
                {'text': 'To create databases', 'is_correct': False},
                {'text': 'To handle server-side logic', 'is_correct': False},
                {'text': 'To manage user authentication', 'is_correct': False}
            ]
        },
        {
            'text': 'Which method is used to add an element to the end of an array in JavaScript?',
            'options': [
                {'text': 'push()', 'is_correct': True},
                {'text': 'pop()', 'is_correct': False},
                {'text': 'shift()', 'is_correct': False},
                {'text': 'unshift()', 'is_correct': False}
            ]
        }
    ]
    
    # Create new questions
    for i, question_data in enumerate(new_questions, 1):
        question = Question.objects.create(
            quiz=demo_quiz,
            text=question_data['text'],
            question_type='multiple-choice'
        )
        
        # Create options for this question
        for option_data in question_data['options']:
            Option.objects.create(
                question=question,
                text=option_data['text'],
                is_correct=option_data['is_correct']
            )
        
        print(f"Created question {i}: {question_data['text']}")
    
    print(f"Successfully updated {len(new_questions)} questions!")

if __name__ == '__main__':
    update_questions() 