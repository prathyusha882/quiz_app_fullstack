from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch, Avg, Count, Q
from django.db.models.functions import Cast
from django.db.models import FloatField
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from quizzes.models import Quiz, Question, Option
from .models import QuizAttempt, UserAnswer, Certificate, Leaderboard, QuizAnalytics
from .serializers import (
    QuizAttemptSerializer, 
    QuizAttemptCreateSerializer,
    QuizAttemptSubmitSerializer,
    UserAnswerSerializer,
    CertificateSerializer,
    CertificateCreateSerializer,
    LeaderboardSerializer,
    QuizAnalyticsSerializer,
    ManualGradingSerializer,
    ProgressTrackingSerializer,
    UserStatsSerializer,
    QuizResultSummarySerializer,
    AnswerReviewSerializer,
    ExportResultsSerializer
)
from .tasks import process_quiz_completion

# -------------------------------
# 🎯 QUIZ ATTEMPT MANAGEMENT
# -------------------------------

class QuizAttemptCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuizAttemptCreateSerializer

    def post(self, request, quiz_id):
        try:
            quiz = Quiz.objects.get(id=quiz_id, is_active=True, status='published')
            
            # Check if user can attempt this quiz
            can_attempt, message = quiz.can_user_attempt(request.user)
            if not can_attempt:
                return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
            
            # Create attempt
            attempt_data = {
                'quiz': quiz,
                'user': request.user
            }
            serializer = self.serializer_class(data=attempt_data, context={'request': request})
            if serializer.is_valid():
                attempt = serializer.save()
                return Response(QuizAttemptSerializer(attempt).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Quiz.DoesNotExist:
            return Response({"detail": "Quiz not found."}, status=status.HTTP_404_NOT_FOUND)

class QuizSubmitView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuizAttemptSubmitSerializer

    def post(self, request, quiz_id):
        user = request.user
        quiz = get_object_or_404(Quiz, pk=quiz_id, is_active=True)
        submitted_answers_data = request.data.get('answers', [])
        time_taken = request.data.get('timeTaken', '00:00')

        print(f"Received data: {request.data}")
        print(f"Answers: {submitted_answers_data}")

        if not isinstance(submitted_answers_data, list):
            return Response({"error": "Answers must be a list of objects."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # Get or create attempt
            attempt, created = QuizAttempt.objects.get_or_create(
                user=user,
                quiz=quiz,
                defaults={
                    'total_questions': quiz.questions.count(),
                    'time_taken': time_taken
                }
            )

            score = 0
            questions_for_quiz = {q.id: q for q in quiz.questions.all().prefetch_related('options')}

            for submitted_answer_entry in submitted_answers_data:
                print(f"Processing answer: {submitted_answer_entry}")
                
                question_id = submitted_answer_entry.get('question_id')
                user_submitted_answer = submitted_answer_entry.get('submitted_answer') or submitted_answer_entry.get('selected_answer')
                
                if not question_id or user_submitted_answer is None:
                    print(f"Skipping invalid answer: {submitted_answer_entry}")
                    continue

                question = questions_for_quiz.get(int(question_id))
                if not question:
                    print(f"Question not found: {question_id}")
                    continue

                # Create user answer
                user_answer = UserAnswer.objects.create(
                    attempt=attempt,
                    question=question
                )

                # Grade the answer
                if question.question_type == 'multiple-choice':
                    chosen_option = question.options.filter(text=user_submitted_answer).first()
                    if chosen_option:
                        user_answer.chosen_options.add(chosen_option)
                        if chosen_option.is_correct:
                            score += 1
                            user_answer.is_correct_answer = True
                elif question.question_type == 'checkbox':
                    user_selected_options = question.options.filter(text__in=user_submitted_answer)
                    user_answer.chosen_options.set(user_selected_options)
                    correct_options = question.correct_options
                    if set(user_selected_options) == set(correct_options):
                        score += 1
                        user_answer.is_correct_answer = True
                elif question.question_type in ['text-input', 'essay']:
                    user_answer.text_answer = user_submitted_answer
                    # For text input, check against correct options
                    correct_texts = [opt.text.strip().lower() for opt in question.correct_options]
                    if str(user_submitted_answer).strip().lower() in correct_texts:
                        score += 1
                        user_answer.is_correct_answer = True
                elif question.question_type == 'file-upload':
                    # Handle file upload - requires manual grading
                    user_answer.uploaded_file = user_submitted_answer
                    user_answer.is_manually_graded = True

                user_answer.grade_answer()
                user_answer.save()

            # Update attempt
            attempt.score = score
            attempt.correct_answers = score
            attempt.incorrect_answers = attempt.total_questions - score
            attempt.percentage_score = (score / attempt.total_questions) * 100 if attempt.total_questions > 0 else 0
            attempt.passed = attempt.percentage_score >= quiz.passing_score
            attempt.is_completed = True
            attempt.is_submitted = True
            attempt.submitted_at = timezone.now()
            attempt.save()

            # Process quiz completion asynchronously
            process_quiz_completion.delay(attempt.id)

            serializer = QuizAttemptSerializer(attempt)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# -------------------------------
# 📊 RESULTS & ANALYTICS
# -------------------------------

class UserResultsListView(generics.ListAPIView):
    serializer_class = QuizAttemptSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['quiz', 'passed', 'is_completed']
    search_fields = ['quiz__title']
    ordering_fields = ['submitted_at', 'score', 'percentage_score']

    def get_queryset(self):
        return QuizAttempt.objects.filter(user=self.request.user).select_related('quiz')

class QuizAttemptDetailView(generics.RetrieveAPIView):
    serializer_class = QuizAttemptSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return QuizAttempt.objects.filter(user=self.request.user).select_related('quiz')

class QuizAttemptReviewView(generics.RetrieveAPIView):
    serializer_class = AnswerReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserAnswer.objects.filter(attempt__user=self.request.user).select_related('question', 'attempt')

class AdminResultsListView(generics.ListAPIView):
    queryset = QuizAttempt.objects.all().order_by('-submitted_at').select_related('user', 'quiz')
    serializer_class = QuizAttemptSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['quiz', 'user', 'passed', 'is_completed', 'is_valid']
    search_fields = ['user__username', 'quiz__title']
    ordering_fields = ['submitted_at', 'score', 'percentage_score']

# -------------------------------
# 📈 PROGRESS TRACKING
# -------------------------------

class UserProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        
        # Calculate progress statistics
        total_quizzes_taken = QuizAttempt.objects.filter(user=user, is_completed=True).count()
        total_score = QuizAttempt.objects.filter(user=user, is_completed=True).aggregate(
            total=Avg('percentage_score')
        )['total'] or 0
        average_score = total_score
        
        # Get certificates earned
        certificates_earned = Certificate.objects.filter(attempt__user=user).count()
        
        # Get quizzes passed
        quizzes_passed = QuizAttempt.objects.filter(user=user, passed=True).count()
        
        # Calculate total time spent
        total_time_spent = QuizAttempt.objects.filter(
            user=user, 
            is_completed=True,
            time_taken__isnull=False
        ).aggregate(
            total_time=Avg('time_taken')
        )['total_time']
        
        # Get recent attempts
        recent_attempts = QuizAttempt.objects.filter(
            user=user, 
            is_completed=True
        ).select_related('quiz').order_by('-submitted_at')[:5]
        
        # Performance by difficulty
        performance_by_difficulty = QuizAttempt.objects.filter(
            user=user, 
            is_completed=True
        ).values('quiz__difficulty').annotate(
            avg_score=Avg('percentage_score'),
            attempts=Count('id')
        )
        
        # Performance by tag
        performance_by_tag = QuizAttempt.objects.filter(
            user=user, 
            is_completed=True
        ).values('quiz__tags__name').annotate(
            avg_score=Avg('percentage_score'),
            attempts=Count('id')
        )
        
        progress_data = {
            'total_quizzes_taken': total_quizzes_taken,
            'total_score': total_score,
            'average_score': round(average_score, 2),
            'certificates_earned': certificates_earned,
            'quizzes_passed': quizzes_passed,
            'total_time_spent': total_time_spent,
            'recent_attempts': QuizAttemptSerializer(recent_attempts, many=True).data,
            'performance_by_difficulty': list(performance_by_difficulty),
            'performance_by_tag': list(performance_by_tag)
        }
        
        serializer = ProgressTrackingSerializer(progress_data)
        return Response(serializer.data)

# -------------------------------
# 🏆 LEADERBOARD
# -------------------------------

class LeaderboardView(generics.ListAPIView):
    serializer_class = LeaderboardSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['quiz']
    ordering_fields = ['rank', 'score', 'percentage_score', 'time_taken']

    def get_queryset(self):
        quiz_id = self.kwargs.get('quiz_id')
        if quiz_id:
            return Leaderboard.objects.filter(quiz_id=quiz_id)
        return Leaderboard.objects.all()

# -------------------------------
# 📜 CERTIFICATES
# -------------------------------

class CertificateListView(generics.ListAPIView):
    serializer_class = CertificateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Certificate.objects.filter(attempt__user=self.request.user).select_related('attempt', 'attempt__quiz')

class CertificateDetailView(generics.RetrieveAPIView):
    serializer_class = CertificateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'certificate_id'

    def get_queryset(self):
        return Certificate.objects.filter(attempt__user=self.request.user).select_related('attempt', 'attempt__quiz')

# -------------------------------
# 📊 ANALYTICS
# -------------------------------

class QuizAnalyticsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, quiz_id):
        try:
            quiz = Quiz.objects.get(id=quiz_id)
            from .services import CertificateService
            
            # Update analytics
            analytics = CertificateService.update_quiz_analytics(quiz)
            serializer = QuizAnalyticsSerializer(analytics)
            return Response(serializer.data)
        except Quiz.DoesNotExist:
            return Response({"detail": "Quiz not found."}, status=status.HTTP_404_NOT_FOUND)

# -------------------------------
# ✏️ MANUAL GRADING
# -------------------------------

class ManualGradingView(generics.UpdateAPIView):
    serializer_class = ManualGradingSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return UserAnswer.objects.filter(is_manually_graded=True)

# -------------------------------
# 📤 EXPORT RESULTS
# -------------------------------

class ExportResultsView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = ExportResultsSerializer(data=request.data)
        if serializer.is_valid():
            # Handle export logic here
            return Response({"message": "Results exported successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
