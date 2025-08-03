from django.urls import path
from .views import (
    QuizListCreateView,
    QuizRetrieveUpdateDestroyView,
    QuestionListCreateView,
    QuestionRetrieveUpdateDestroyView,
    UserQuizListView,
    UserQuizQuestionsView,
    quiz_detail,
    QuizAnalyticsView,
    GlobalAnalyticsView,
    TagListView,
    TagDetailView,
    QuestionBankView,
    QuestionImportView,
    QuizExportView,
    QuizSessionView,
    QuizSearchView,
)

urlpatterns = [
    # --- User-facing Quiz APIs ---
    path('', UserQuizListView.as_view(), name='user_quiz_list'),
    path('search/', QuizSearchView.as_view(), name='quiz_search'),
    path('<int:pk>/', quiz_detail, name='quiz-detail'), 
    path('<int:pk>/questions/', UserQuizQuestionsView.as_view(), name='user_quiz_questions'),
    path('<int:quiz_id>/session/', QuizSessionView.as_view(), name='quiz_session'),

    # --- Admin Quiz APIs ---
    path('admin/', QuizListCreateView.as_view(), name='admin_quiz_list_create'),
    path('admin/<int:pk>/', QuizRetrieveUpdateDestroyView.as_view(), name='admin_quiz_retrieve_update_destroy'),
    path('admin/<int:quiz_id>/analytics/', QuizAnalyticsView.as_view(), name='quiz_analytics'),
    path('admin/analytics/global/', GlobalAnalyticsView.as_view(), name='global_analytics'),

    # --- Admin Question APIs ---
    path('admin/<int:quiz_pk>/questions/', QuestionListCreateView.as_view(), name='admin_question_list_create'),
    path('admin/<int:quiz_pk>/questions/<int:pk>/', QuestionRetrieveUpdateDestroyView.as_view(), name='admin_question_retrieve_update_destroy'),

    # --- Tag Management ---
    path('admin/tags/', TagListView.as_view(), name='tag_list'),
    path('admin/tags/<int:pk>/', TagDetailView.as_view(), name='tag_detail'),

    # --- Question Bank ---
    path('admin/questions/', QuestionBankView.as_view(), name='question_bank'),

    # --- Import/Export ---
    path('admin/import/', QuestionImportView.as_view(), name='question_import'),
    path('admin/export/', QuizExportView.as_view(), name='quiz_export'),
]
