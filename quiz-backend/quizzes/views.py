# quizzes/views.py

import random
# import requests  # Temporarily commented out
from django.shortcuts import get_object_or_404, redirect
from django.db import transaction
from django.contrib import messages
from django.template.response import TemplateResponse

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError

from .models import Quiz, Question, Option
from .serializers import (
    QuizSerializer,
    QuestionSerializer,
    TakeQuizQuestionSerializer,
    AdminQuestionDetailSerializer,
)

# -------------------------------
# 👤 USER QUIZ VIEWS
# -------------------------------

class UserQuizListView(generics.ListAPIView):
    queryset = Quiz.objects.filter(is_active=True).prefetch_related('questions')
    serializer_class = QuizSerializer
    permission_classes = (AllowAny,)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def quiz_detail(request, pk):
    try:
        quiz = Quiz.objects.get(pk=pk)
        serializer = QuizSerializer(quiz)
        return Response(serializer.data)
    except Quiz.DoesNotExist:
        return Response({"detail": "Quiz not found."}, status=status.HTTP_404_NOT_FOUND)

class UserQuizQuestionsView(generics.ListAPIView):
    serializer_class = TakeQuizQuestionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        quiz_id = self.kwargs['pk']
        quiz = get_object_or_404(Quiz.objects.filter(is_active=True), id=quiz_id)
        all_questions = list(quiz.questions.all().prefetch_related('options'))

        # Get user-specific seed for consistent randomization per user
        user_id = self.request.user.id
        import random
        random.seed(user_id)  # This ensures same user gets same questions
        
        NUM_QUESTIONS_PER_ATTEMPT = 5  # Increased from 3 to 5
        
        if len(all_questions) <= NUM_QUESTIONS_PER_ATTEMPT:
            selected_questions = all_questions
        else:
            selected_questions = random.sample(all_questions, NUM_QUESTIONS_PER_ATTEMPT)
        
        # Shuffle options for each question to make it different for each student
        for question in selected_questions:
            options = list(question.options.all())
            random.shuffle(options)
            # Temporarily store shuffled options
            question._shuffled_options = options
        
        return selected_questions

# -------------------------------
# 🛠️ ADMIN QUIZ CRUD VIEWS
# -------------------------------

class QuizListCreateView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all().order_by('-created_at')
    serializer_class = QuizSerializer
    permission_classes = (IsAdminUser,)

    def perform_create(self, serializer):
        serializer.save()

class QuizRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = 'pk'

# -------------------------------
# 🛠️ ADMIN QUESTION CRUD VIEWS
# -------------------------------

class QuestionListCreateView(generics.ListCreateAPIView):
    serializer_class = AdminQuestionDetailSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        quiz_pk = self.kwargs['quiz_pk']
        return Question.objects.filter(quiz_id=quiz_pk).prefetch_related('options')

    def perform_create(self, serializer):
        quiz_pk = self.kwargs['quiz_pk']
        quiz = get_object_or_404(Quiz, pk=quiz_pk)
        question_type = serializer.validated_data.get('question_type')
        options_data = serializer.validated_data.get('options')

        if question_type in ['multiple-choice', 'checkbox']:
            if not options_data:
                raise ValidationError({"options": "Options are required."})
            correct_count = sum(1 for opt in options_data if opt.get('is_correct'))
            if correct_count == 0:
                raise ValidationError({"options": "At least one correct option required."})
            if question_type == 'multiple-choice' and correct_count > 1:
                raise ValidationError({"options": "Only one correct option allowed."})
        elif question_type == 'text-input' and options_data:
            if len(options_data) > 1 or not options_data[0].get('text'):
                raise ValidationError({"options": "Only one correct text answer allowed."})
            if not options_data[0].get('is_correct'):
                options_data[0]['is_correct'] = True

        serializer.save(quiz=quiz)

class QuestionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AdminQuestionDetailSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = 'pk'

    def get_queryset(self):
        quiz_pk = self.kwargs['quiz_pk']
        return Question.objects.filter(quiz_id=quiz_pk).prefetch_related('options')

    def perform_update(self, serializer):
        question_type = serializer.validated_data.get('question_type', serializer.instance.question_type)
        options_data = serializer.validated_data.get('options')

        if question_type in ['multiple-choice', 'checkbox']:
            if options_data is None:
                pass
            elif not options_data:
                raise ValidationError({"options": "Options are required."})
            else:
                correct_count = sum(1 for opt in options_data if opt.get('is_correct'))
                if correct_count == 0:
                    raise ValidationError({"options": "At least one correct option required."})
                if question_type == 'multiple-choice' and correct_count > 1:
                    raise ValidationError({"options": "Only one correct option allowed."})
        elif question_type == 'text-input' and options_data:
            if len(options_data) > 1 or not options_data[0].get('text'):
                raise ValidationError({"options": "Only one correct text answer allowed."})
            if not options_data[0].get('is_correct', False):
                options_data[0]['is_correct'] = True

        serializer.save()

# -------------------------------
# 🤖 AI QUESTION GENERATION VIEW
# -------------------------------

# @api_view(['POST'])
# @permission_classes([IsAdminUser])
# def generate_ai_questions_view(request):
#     quiz_id = request.data.get('quiz_id')
#     topic = request.data.get('topic')
#     difficulty = request.data.get('difficulty')
#     num_questions = int(request.data.get('num_questions', 5))

#     if not quiz_id or not topic or not difficulty:
#         return Response({"error": "Missing required fields."}, status=400)

#     quiz = get_object_or_404(Quiz, pk=quiz_id)

#     prompt = (
#         f"Generate {num_questions} multiple choice questions on the topic '{topic}' "
#         f"for {difficulty} level. Include 4 options and indicate the correct one."
#     )

#     try:
#         response = requests.post(
#             'http://localhost:11434/api/generate',
#             json={"model": "llama3", "prompt": prompt, "stream": False},
#             timeout=60
#         )
#         data = response.json()
#         content = data.get('response', '')

#         print("🧠 Raw Ollama Output:\n", content)
#         messages.success(request, "Questions generated (check console). Parser not yet applied.")

#         return redirect('/admin/quizzes/question/')

#     except Exception as e:
#         messages.error(request, f"Error generating questions: {e}")
#         return redirect('/admin/quizzes/question/')

# -------------------------------
# 📝 QUIZ REVIEW VIEW
# -------------------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def QuizAttemptReviewView(request, quiz_id, result_id):
    """
    Given a quiz ID and result ID (attempt), return the review information:
    - quiz title
    - list of questions
    - user's selected answers
    - correct answers
    """
    # For now, assuming result_id is a datetime string (or could be used to find stored attempt)
    # In production, use a real QuizResult model
    try:
        quiz = Quiz.objects.prefetch_related('questions__options').get(id=quiz_id)
        questions = quiz.questions.all()

        # Fake placeholder response (simulate previous attempt)
        review_data = {
            "quiz_title": quiz.title,
            "questions_for_review": [
                {
                    "id": question.id,
                    "text": question.text,
                    "type": question.question_type,
                    "options": [opt.text for opt in question.options.all()],
                    "correct_answers": [opt.text for opt in question.options.filter(is_correct=True)],
                    "user_chosen_option_text": [opt.text for opt in question.options.filter(is_correct=True)],
                }
                for question in questions
            ],
        }

        return Response(review_data)

    except Quiz.DoesNotExist:
        return Response({"detail": "Quiz not found"}, status=404)
