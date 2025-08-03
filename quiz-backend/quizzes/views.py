# quizzes/views.py

import random
# import requests  # Temporarily commented out
from django.shortcuts import get_object_or_404, redirect
from django.db import transaction
from django.contrib import messages
from django.template.response import TemplateResponse
from django.utils import timezone
from django.db.models import Q, Count, Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView

from .models import Quiz, Question, Option, Tag, QuizSession
from .serializers import (
    QuizListSerializer,
    QuizDetailSerializer,
    QuizCreateSerializer,
    QuizUpdateSerializer,
    QuestionSerializer,
    QuestionCreateSerializer,
    QuizSessionSerializer,
    QuizFilterSerializer,
    QuestionBankSerializer,
    QuestionImportSerializer,
    QuizExportSerializer,
    QuizAnalyticsSerializer,
)

# -------------------------------
# 👤 USER QUIZ VIEWS
# -------------------------------

class UserQuizListView(generics.ListAPIView):
    queryset = Quiz.objects.filter(is_active=True, status='published').prefetch_related('questions', 'tags')
    serializer_class = QuizListSerializer
    permission_classes = (AllowAny,)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['difficulty', 'tags', 'created_by']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title', 'difficulty']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Apply filters
        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        tags = self.request.query_params.getlist('tags')
        if tags:
            queryset = queryset.filter(tags__id__in=tags)
        
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search) |
                Q(tags__name__icontains=search)
            ).distinct()
        
        return queryset

@api_view(['GET'])
@permission_classes([AllowAny])
def quiz_detail(request, pk):
    try:
        quiz = Quiz.objects.get(pk=pk, is_active=True, status='published')
        serializer = QuizDetailSerializer(quiz, context={'request': request})
        return Response(serializer.data)
    except Quiz.DoesNotExist:
        return Response({"detail": "Quiz not found."}, status=status.HTTP_404_NOT_FOUND)

class UserQuizQuestionsView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        quiz_id = self.kwargs['pk']
        quiz = get_object_or_404(Quiz.objects.filter(is_active=True, status='published'), id=quiz_id)
        all_questions = list(quiz.questions.all().prefetch_related('options').order_by('order'))

        # Get user-specific seed for consistent randomization per user
        user_id = self.request.user.id
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
    serializer_class = QuizListSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'difficulty', 'created_by', 'tags']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title', 'difficulty']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return QuizCreateSerializer
        return QuizListSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class QuizRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizDetailSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return QuizUpdateSerializer
        return QuizDetailSerializer

# -------------------------------
# 🛠️ ADMIN QUESTION CRUD VIEWS
# -------------------------------

class QuestionListCreateView(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        quiz_pk = self.kwargs['quiz_pk']
        return Question.objects.filter(quiz_id=quiz_pk).order_by('order')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return QuestionCreateSerializer
        return QuestionSerializer

    def perform_create(self, serializer):
        quiz_pk = self.kwargs['quiz_pk']
        quiz = get_object_or_404(Quiz, pk=quiz_pk)
        serializer.save(quiz=quiz)

class QuestionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = 'pk'

    def get_queryset(self):
        quiz_pk = self.kwargs['quiz_pk']
        return Question.objects.filter(quiz_id=quiz_pk)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return QuestionCreateSerializer
        return QuestionSerializer

    def perform_update(self, serializer):
        serializer.save()

# -------------------------------
# 📊 QUIZ ANALYTICS & STATISTICS
# -------------------------------

class QuizAnalyticsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, quiz_id):
        try:
            quiz = Quiz.objects.get(id=quiz_id)
            from results.models import QuizAnalytics
            from results.services import CertificateService
            
            # Update analytics
            analytics = CertificateService.update_quiz_analytics(quiz)
            serializer = QuizAnalyticsSerializer(analytics)
            return Response(serializer.data)
        except Quiz.DoesNotExist:
            return Response({"detail": "Quiz not found."}, status=status.HTTP_404_NOT_FOUND)

class GlobalAnalyticsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_quizzes = Quiz.objects.count()
        active_quizzes = Quiz.objects.filter(is_active=True).count()
        published_quizzes = Quiz.objects.filter(status='published').count()
        
        from results.models import QuizAttempt
        total_attempts = QuizAttempt.objects.count()
        completed_attempts = QuizAttempt.objects.filter(is_completed=True).count()
        
        avg_score = QuizAttempt.objects.filter(is_completed=True).aggregate(
            avg_score=Avg('percentage_score')
        )['avg_score'] or 0
        
        recent_activity = QuizAttempt.objects.filter(
            submitted_at__gte=timezone.now() - timezone.timedelta(days=7)
        ).count()
        
        return Response({
            'total_quizzes': total_quizzes,
            'active_quizzes': active_quizzes,
            'published_quizzes': published_quizzes,
            'total_attempts': total_attempts,
            'completed_attempts': completed_attempts,
            'average_score': round(avg_score, 2),
            'recent_activity': recent_activity
        })

# -------------------------------
# 🏷️ TAG MANAGEMENT
# -------------------------------

class TagListView(generics.ListCreateAPIView):
    from .serializers import TagSerializer
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer
    permission_classes = [IsAdminUser]

class TagDetailView(generics.RetrieveUpdateDestroyAPIView):
    from .serializers import TagSerializer
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUser]

# -------------------------------
# 📚 QUESTION BANK
# -------------------------------

class QuestionBankView(generics.ListAPIView):
    serializer_class = QuestionBankSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['question_type', 'quiz']
    search_fields = ['text']

    def get_queryset(self):
        return Question.objects.all().prefetch_related('quiz_set')

# -------------------------------
# 📥 IMPORT/EXPORT
# -------------------------------

class QuestionImportView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = QuestionImportSerializer(data=request.data)
        if serializer.is_valid():
            # Handle file import logic here
            return Response({"message": "Questions imported successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuizExportView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = QuizExportSerializer(data=request.data)
        if serializer.is_valid():
            # Handle export logic here
            return Response({"message": "Quiz exported successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -------------------------------
# 🎯 QUIZ SESSIONS
# -------------------------------

class QuizSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, quiz_id):
        try:
            quiz = Quiz.objects.get(id=quiz_id, is_active=True, status='published')
            
            # Check if user can attempt this quiz
            can_attempt, message = quiz.can_user_attempt(request.user)
            if not can_attempt:
                return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
            
            # Create or get existing session
            session, created = QuizSession.objects.get_or_create(
                user=request.user,
                quiz=quiz,
                is_active=True
            )
            
            serializer = QuizSessionSerializer(session)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Quiz.DoesNotExist:
            return Response({"detail": "Quiz not found."}, status=status.HTTP_404_NOT_FOUND)

# -------------------------------
# 🔍 SEARCH & FILTER
# -------------------------------

class QuizSearchView(generics.ListAPIView):
    serializer_class = QuizListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['difficulty', 'tags', 'status']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title', 'difficulty']

    def get_queryset(self):
        return Quiz.objects.filter(is_active=True, status='published').prefetch_related('questions', 'tags')
