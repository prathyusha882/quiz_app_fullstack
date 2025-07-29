# quiz-backend/quizzes/urls.py
from django.urls import path
from .views import (
    QuizListCreateView, QuizRetrieveUpdateDestroyView,
    QuestionListCreateView, QuestionRetrieveUpdateDestroyView,
    UserQuizListView, UserQuizDetailView, UserQuizQuestionsView
)

urlpatterns = [
    # User-facing Quiz APIs (read-only for all, or authenticated read-only)
    path('', UserQuizListView.as_view(), name='user_quiz_list'),
    path('<int:pk>/', UserQuizDetailView.as_view(), name='user_quiz_detail'),
    path('<int:pk>/questions/', UserQuizQuestionsView.as_view(), name='user_quiz_questions'), # Get questions for taking quiz

    # Admin Quiz APIs (CRUD operations)
    path('admin/quizzes/', QuizListCreateView.as_view(), name='admin_quiz_list_create'),
    path('admin/quizzes/<int:pk>/', QuizRetrieveUpdateDestroyView.as_view(), name='admin_quiz_retrieve_update_destroy'),

    # Admin Question APIs (CRUD operations for questions within a quiz)
    # Note: quiz_pk is the ID of the parent quiz
    path('admin/quizzes/<int:quiz_pk>/questions/', QuestionListCreateView.as_view(), name='admin_question_list_create'),
    path('admin/quizzes/<int:quiz_pk>/questions/<int:pk>/', QuestionRetrieveUpdateDestroyView.as_view(), name='admin_question_retrieve_update_destroy'),
]