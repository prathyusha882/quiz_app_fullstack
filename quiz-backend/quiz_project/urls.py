from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse  # ✅ For a default welcome response

# ✅ Default homepage response
def homepage(request):
    return HttpResponse("Welcome to the Quiz App backend!")

urlpatterns = [
    path('', homepage),  # ✅ Default route
    path('admin/', admin.site.urls),

    # ✅ User authentication APIs
    path('api/auth/', include('users.urls')),

    # ✅ Quiz APIs (user + admin + AI generation)
    path('api/quizzes/', include('quizzes.urls')),

    # ✅ Results/score-related APIs
    path('api/results/', include('results.urls')),
]
