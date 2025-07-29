from django.shortcuts import render

# Create your views here.
# quiz-backend/quizzes/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from .models import Quiz, Question, Option
from .serializers import (
    QuizSerializer, QuestionSerializer, TakeQuizQuestionSerializer,
    AdminQuestionDetailSerializer
)
from users.permissions import IsAdminOrReadOnly # Assuming you have this permission

# --- Permissions Helper (optional, but good for fine-grained control) ---
# Create this file users/permissions.py if you haven't already
# (Though for this example, we'll just use IsAdminUser where needed)
"""
# users/permissions.py
from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    
    # Custom permission to only allow admins to edit/create.
    # Read-only access is allowed for anyone.
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True # Read permissions are allowed to any request
        return request.user and request.user.is_staff # Write permissions only to staff (admin)
"""


# --- User-facing Quiz Views ---

class UserQuizListView(generics.ListAPIView):
    """
    List all active quizzes for users.
    Only active quizzes are shown.
    """
    queryset = Quiz.objects.filter(is_active=True).prefetch_related('questions')
    serializer_class = QuizSerializer
    permission_classes = (AllowAny,) # Allow any user to see the list

class UserQuizDetailView(generics.RetrieveAPIView):
    """
    Retrieve details of a single active quiz for users.
    """
    queryset = Quiz.objects.filter(is_active=True).prefetch_related('questions')
    serializer_class = QuizSerializer
    permission_classes = (IsAuthenticated,) # Require authentication to see details

class UserQuizQuestionsView(generics.ListAPIView):
    """
    List questions for a specific quiz for taking.
    Excludes correct answers. Requires authentication.
    """
    serializer_class = TakeQuizQuestionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        quiz_id = self.kwargs['pk'] # 'pk' refers to the quiz ID from the URL
        # Ensure the quiz exists and is active
        quiz = get_object_or_404(Quiz.objects.filter(is_active=True), id=quiz_id)
        return quiz.questions.all().prefetch_related('options') # Fetch questions with options


# --- Admin Quiz Management Views ---

class QuizListCreateView(generics.ListCreateAPIView):
    """
    Admin endpoint to list all quizzes or create a new quiz.
    Requires admin privileges.
    """
    queryset = Quiz.objects.all().order_by('-created_at')
    serializer_class = QuizSerializer
    permission_classes = (IsAdminUser,) # Only admin users can access this view

    def perform_create(self, serializer):
        # Additional logic before saving if needed
        serializer.save()

class QuizRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Admin endpoint to retrieve, update, or delete a specific quiz.
    Requires admin privileges.
    """
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = 'pk' # Use 'pk' to match URL pattern


# --- Admin Question Management Views ---

class QuestionListCreateView(generics.ListCreateAPIView):
    """
    Admin endpoint to list questions for a specific quiz or create a new question for it.
    Requires admin privileges.
    """
    serializer_class = AdminQuestionDetailSerializer # Use serializer that includes is_correct for admin
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        quiz_pk = self.kwargs['quiz_pk']
        quiz = get_object_or_404(Quiz, pk=quiz_pk)
        return quiz.questions.all().prefetch_related('options')

    def perform_create(self, serializer):
        quiz_pk = self.kwargs['quiz_pk']
        quiz = get_object_or_404(Quiz, pk=quiz_pk)
        # Check if question type is valid for options
        question_type = serializer.validated_data.get('question_type')
        options_data = serializer.validated_data.get('options')

        if question_type in ['multiple-choice', 'checkbox']:
            if not options_data:
                raise ValidationError({"options": "Options are required for this question type."})
            correct_options_count = sum(1 for opt in options_data if opt.get('is_correct'))
            if correct_options_count == 0:
                raise ValidationError({"options": "At least one correct option is required."})
            if question_type == 'multiple-choice' and correct_options_count > 1:
                 raise ValidationError({"options": "Multiple-choice questions can only have one correct option."})
        elif question_type == 'text-input' and options_data:
            # For text-input, options should ideally be just one correct answer string.
            # We can adjust this if needed, or simply take the first option as the correct answer string.
            if len(options_data) > 1 or not options_data[0].get('text'):
                 raise ValidationError({"options": "Text input questions should have a single text correct answer."})
            # Ensure is_correct is true for text input if provided
            if options_data and not options_data[0].get('is_correct', False):
                options_data[0]['is_correct'] = True # Force text input correct answer to be true
        
        serializer.save(quiz=quiz) # Associate question with the quiz


class QuestionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Admin endpoint to retrieve, update, or delete a specific question for a quiz.
    Requires admin privileges.
    """
    serializer_class = AdminQuestionDetailSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = 'pk' # Matches the <int:pk> in URL

    def get_queryset(self):
        quiz_pk = self.kwargs['quiz_pk']
        # Ensure the question belongs to the specified quiz
        return Question.objects.filter(quiz_id=quiz_pk).prefetch_related('options')

    def perform_update(self, serializer):
        question_type = serializer.validated_data.get('question_type', serializer.instance.question_type)
        options_data = serializer.validated_data.get('options')

        if question_type in ['multiple-choice', 'checkbox']:
            if options_data is None: # If options are not provided, it means no change to options, so allow
                pass
            elif not options_data:
                raise ValidationError({"options": "Options are required for this question type."})
            else:
                correct_options_count = sum(1 for opt in options_data if opt.get('is_correct'))
                if correct_options_count == 0:
                    raise ValidationError({"options": "At least one correct option is required."})
                if question_type == 'multiple-choice' and correct_options_count > 1:
                     raise ValidationError({"options": "Multiple-choice questions can only have one correct option."})
        elif question_type == 'text-input' and options_data:
            if len(options_data) > 1 or not options_data[0].get('text'):
                 raise ValidationError({"options": "Text input questions should have a single text correct answer."})
            if options_data and not options_data[0].get('is_correct', False):
                options_data[0]['is_correct'] = True # Force text input correct answer to be true

        serializer.save()