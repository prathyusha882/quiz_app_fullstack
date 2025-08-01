#!/usr/bin/env python
"""
Script to create proper quiz content with meaningful questions and options.
Run this from the quiz-backend directory.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
django.setup()

from quizzes.models import Quiz, Question, Option

def create_proper_quiz_content():
    """Create proper quiz content with meaningful questions and options."""
    
    # Clear existing content
    print("Clearing existing quiz content...")
    Quiz.objects.all().delete()
    
    # Create a comprehensive quiz
    quiz = Quiz.objects.create(
        title="General Knowledge Quiz",
        description="Test your knowledge across various subjects including geography, science, and technology.",
        difficulty="Medium",
        duration=900,  # 15 minutes
        is_active=True
    )
    
    # Sample questions with proper options - Multiple questions per topic
    questions_data = [
        # Programming Languages - Multiple questions
        {
            "text": "Which programming language is known as the 'language of the web'?",
            "options": [
                ("JavaScript", True),
                ("Python", False),
                ("Java", False),
                ("C++", False)
            ]
        },
        {
            "text": "What is the primary use of Python in web development?",
            "options": [
                ("Backend development", True),
                ("Frontend styling", False),
                ("Database design", False),
                ("Mobile apps", False)
            ]
        },
        {
            "text": "Which language is commonly used for Android app development?",
            "options": [
                ("Java", True),
                ("JavaScript", False),
                ("Python", False),
                ("PHP", False)
            ]
        },
        {
            "text": "What is the main advantage of using C++?",
            "options": [
                ("High performance", True),
                ("Easy learning curve", False),
                ("Built-in web features", False),
                ("Automatic memory management", False)
            ]
        },
        
        # Web Technologies - Multiple questions
        {
            "text": "Which company developed the React.js framework?",
            "options": [
                ("Facebook", True),
                ("Google", False),
                ("Microsoft", False),
                ("Apple", False)
            ]
        },
        {
            "text": "What is the purpose of Angular framework?",
            "options": [
                ("Building single-page applications", True),
                ("Database management", False),
                ("Server configuration", False),
                ("Mobile development", False)
            ]
        },
        {
            "text": "Which framework is known for its simplicity and flexibility?",
            "options": [
                ("Vue.js", True),
                ("Angular", False),
                ("React", False),
                ("jQuery", False)
            ]
        },
        {
            "text": "What does HTML stand for?",
            "options": [
                ("HyperText Markup Language", True),
                ("High Tech Modern Language", False),
                ("Home Tool Markup Language", False),
                ("Hyperlink and Text Markup Language", False)
            ]
        },
        {
            "text": "What is the primary function of CSS?",
            "options": [
                ("Styling web pages", True),
                ("Database management", False),
                ("Server-side programming", False),
                ("Mobile app development", False)
            ]
        },
        {
            "text": "Which CSS property controls element positioning?",
            "options": [
                ("position", True),
                ("display", False),
                ("margin", False),
                ("padding", False)
            ]
        },
        
        # Databases - Multiple questions
        {
            "text": "Which database is commonly used with Django?",
            "options": [
                ("PostgreSQL", True),
                ("MongoDB", False),
                ("Redis", False),
                ("SQLite", False)
            ]
        },
        {
            "text": "Which of the following is a NoSQL database?",
            "options": [
                ("MongoDB", True),
                ("MySQL", False),
                ("PostgreSQL", False),
                ("SQLite", False)
            ]
        },
        {
            "text": "What is the primary advantage of Redis?",
            "options": [
                ("In-memory data storage", True),
                ("Complex queries", False),
                ("Large file storage", False),
                ("Graph processing", False)
            ]
        },
        {
            "text": "Which database is best for relational data?",
            "options": [
                ("MySQL", True),
                ("MongoDB", False),
                ("Redis", False),
                ("Cassandra", False)
            ]
        },
        
        # DevOps & Tools - Multiple questions
        {
            "text": "What is the purpose of Git?",
            "options": [
                ("Version control", True),
                ("Web hosting", False),
                ("Database management", False),
                ("Email service", False)
            ]
        },
        {
            "text": "What is the purpose of Docker?",
            "options": [
                ("Containerization of applications", True),
                ("Database management", False),
                ("Web hosting", False),
                ("Email services", False)
            ]
        },
        {
            "text": "Which tool is used for continuous integration?",
            "options": [
                ("Jenkins", True),
                ("Docker", False),
                ("Git", False),
                ("Kubernetes", False)
            ]
        },
        {
            "text": "What is Kubernetes used for?",
            "options": [
                ("Container orchestration", True),
                ("Database management", False),
                ("Web development", False),
                ("Version control", False)
            ]
        },
        
        # APIs & Web Services - Multiple questions
        {
            "text": "What is the main purpose of an API?",
            "options": [
                ("To allow different software systems to communicate", True),
                ("To store data in databases", False),
                ("To create user interfaces", False),
                ("To process payments", False)
            ]
        },
        {
            "text": "Which HTTP method is used to create new resources?",
            "options": [
                ("POST", True),
                ("GET", False),
                ("PUT", False),
                ("DELETE", False)
            ]
        },
        {
            "text": "What is the purpose of JWT tokens?",
            "options": [
                ("Authentication and authorization", True),
                ("Data encryption", False),
                ("Database queries", False),
                ("File storage", False)
            ]
        },
        {
            "text": "Which protocol is used for secure web browsing?",
            "options": [
                ("HTTPS", True),
                ("HTTP", False),
                ("FTP", False),
                ("SMTP", False)
            ]
        },
        
        # React & Frontend - Multiple questions
        {
            "text": "Which programming paradigm does React follow?",
            "options": [
                ("Component-based", True),
                ("Object-oriented", False),
                ("Functional", False),
                ("Procedural", False)
            ]
        },
        {
            "text": "What is the purpose of Redux in React applications?",
            "options": [
                ("State management", True),
                ("Routing", False),
                ("Styling", False),
                ("Database operations", False)
            ]
        },
        {
            "text": "Which React hook manages side effects?",
            "options": [
                ("useEffect", True),
                ("useState", False),
                ("useContext", False),
                ("useReducer", False)
            ]
        },
        {
            "text": "What is JSX in React?",
            "options": [
                ("JavaScript XML", True),
                ("JavaScript Extension", False),
                ("JavaScript Syntax", False),
                ("JavaScript Framework", False)
            ]
        },
        
        # Node.js & Backend - Multiple questions
        {
            "text": "What is the purpose of npm in Node.js projects?",
            "options": [
                ("Package management", True),
                ("Database management", False),
                ("Web server", False),
                ("Testing framework", False)
            ]
        },
        {
            "text": "Which of the following is a Node.js framework?",
            "options": [
                ("Express.js", True),
                ("Django", False),
                ("Flask", False),
                ("Laravel", False)
            ]
        },
        {
            "text": "What is the purpose of middleware in Express.js?",
            "options": [
                ("Request processing", True),
                ("Database queries", False),
                ("Frontend rendering", False),
                ("Email sending", False)
            ]
        },
        {
            "text": "Which of the following is a cloud platform?",
            "options": [
                ("AWS", True),
                ("MySQL", False),
                ("MongoDB", False),
                ("Redis", False)
            ]
        },
        {
            "text": "What is the purpose of Azure?",
            "options": [
                ("Cloud computing platform", True),
                ("Database management", False),
                ("Web development", False),
                ("Version control", False)
            ]
        }
    ]
    
    # Create questions and options
    for i, q_data in enumerate(questions_data, 1):
        question = Question.objects.create(
            quiz=quiz,
            text=q_data["text"],
            question_type="multiple-choice"
        )
        
        print(f"Created question {i}: {q_data['text']}")
        
        # Create options for this question
        for option_text, is_correct in q_data["options"]:
            Option.objects.create(
                question=question,
                text=option_text,
                is_correct=is_correct
            )
            print(f"  - Option: {option_text} ({'Correct' if is_correct else 'Incorrect'})")
    
    print(f"\n✅ Created quiz '{quiz.title}' with {len(questions_data)} questions")
    print(f"Quiz ID: {quiz.id}")
    print("You can now access this quiz in the frontend!")

if __name__ == "__main__":
    create_proper_quiz_content() 
    create_proper_quiz_content() 