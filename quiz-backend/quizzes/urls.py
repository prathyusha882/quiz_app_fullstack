from django.urls import path
from .views import (
    QuizListCreateView,
    QuizRetrieveUpdateDestroyView,
    QuestionListCreateView,
    QuestionRetrieveUpdateDestroyView,
    UserQuizListView,
    UserQuizQuestionsView,
    # generate_ai_questions_view,  # Temporarily commented out
    quiz_detail,
    QuizAttemptReviewView,
)

urlpatterns = [
    # --- User-facing Quiz APIs ---
    path('', UserQuizListView.as_view(), name='user_quiz_list'),
    path('<int:pk>/', quiz_detail, name='quiz-detail'), 
    path('<int:pk>/questions/', UserQuizQuestionsView.as_view(), name='user_quiz_questions'),

    # --- Quiz Attempt Review ---
    path('api/results/<int:quiz_id>/<int:result_id>/', QuizAttemptReviewView, name='quiz_review_detail'),  # ✅ Review detail view

    # --- Admin Quiz APIs ---
    path('admin/', QuizListCreateView.as_view(), name='admin_quiz_list_create'),
    path('admin/<int:pk>/', QuizRetrieveUpdateDestroyView.as_view(), name='admin_quiz_retrieve_update_destroy'),

    # --- Admin Question APIs ---
    path('admin/<int:quiz_pk>/questions/', QuestionListCreateView.as_view(), name='admin_question_list_create'),
    path('admin/<int:quiz_pk>/questions/<int:pk>/', QuestionRetrieveUpdateDestroyView.as_view(), name='admin_question_retrieve_update_destroy'),

    # --- AI Question Generation ---
    # path('admin/generate-ai-questions/', generate_ai_questions_view, name='generate_ai_questions'),  # Temporarily commented out
]
