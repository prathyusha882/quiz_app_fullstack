# quiz-backend/results/urls.py
from django.urls import path
from .views import (
    QuizSubmitView,
    UserResultsListView,
    AdminResultsListView,
    QuizAttemptDetailView,
    QuizAttemptReviewView,
    UserProgressView,  # ✅ make sure the comma is here
)

urlpatterns = [
    # User-facing submission and results
    path('submit/<int:quiz_id>/', QuizSubmitView.as_view(), name='quiz_submit'),
    path('my/', UserResultsListView.as_view(), name='user_results_list'),
    path('<int:pk>/', QuizAttemptDetailView.as_view(), name='quiz_attempt_detail'),  # Get specific attempt by ID
    path('<int:attempt_id>/review/', QuizAttemptReviewView.as_view(), name='quiz_attempt_review'),  # Detailed review
    path('progress/', UserProgressView.as_view(), name='user_progress'),  # ✅ Add this line

    # Admin Results APIs
    path('admin/all/', AdminResultsListView.as_view(), name='admin_all_results_list'),
]
