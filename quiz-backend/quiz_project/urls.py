# quiz-backend/quiz_project/urls.py
from django.contrib import admin
from django.urls import path, include # Ensure 'include' is imported

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')), # Includes user authentication/profile URLs
    path('api/quizzes/', include('quizzes.urls')), # Includes quiz and question URLs
    path('api/results/', include('results.urls')), # <-- ADD THIS LINE
]