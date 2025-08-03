# quiz-backend/results/urls.py
from django.urls import path
from .views import (
    QuizAttemptCreateView,
    QuizSubmitView,
    UserResultsListView,
    AdminResultsListView,
    QuizAttemptDetailView,
    QuizAttemptReviewView,
    UserProgressView,
    LeaderboardView,
    CertificateListView,
    CertificateDetailView,
    QuizAnalyticsView,
    ManualGradingView,
    ExportResultsView,
)

urlpatterns = [
    # Quiz Attempt Management
    path('attempts/create/<int:quiz_id>/', QuizAttemptCreateView.as_view(), name='quiz_attempt_create'),
    path('submit/<int:quiz_id>/', QuizSubmitView.as_view(), name='quiz_submit'),
    
    # User Results & Progress
    path('my/', UserResultsListView.as_view(), name='user_results_list'),
    path('<int:pk>/', QuizAttemptDetailView.as_view(), name='quiz_attempt_detail'),
    path('<int:attempt_id>/review/', QuizAttemptReviewView.as_view(), name='quiz_attempt_review'),
    path('progress/', UserProgressView.as_view(), name='user_progress'),
    
    # Leaderboard
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('leaderboard/<int:quiz_id>/', LeaderboardView.as_view(), name='quiz_leaderboard'),
    
    # Certificates
    path('certificates/', CertificateListView.as_view(), name='certificate_list'),
    path('certificates/<str:certificate_id>/', CertificateDetailView.as_view(), name='certificate_detail'),
    
    # Admin Results & Analytics
    path('admin/all/', AdminResultsListView.as_view(), name='admin_all_results_list'),
    path('admin/analytics/<int:quiz_id>/', QuizAnalyticsView.as_view(), name='quiz_analytics'),
    path('admin/grading/', ManualGradingView.as_view(), name='manual_grading'),
    path('admin/export/', ExportResultsView.as_view(), name='export_results'),
]
