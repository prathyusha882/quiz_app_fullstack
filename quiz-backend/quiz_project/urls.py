from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse  # ✅ For a default welcome response
from django.conf import settings
from django.conf.urls.static import static

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

    # ✅ OAuth and Social Authentication
    path('accounts/', include('allauth.urls')),
    path('api/social/', include('allauth.socialaccount.urls')),

    # ✅ Course APIs
    path('api/courses/', include('courses.urls')),

    # ✅ Payment APIs
    path('api/payments/', include('payments.urls')),

    # ✅ Analytics APIs
    path('api/analytics/', include('analytics.urls')),

    # ✅ Proctoring APIs
    path('api/proctoring/', include('proctoring.urls')),

    # ✅ Rich text editor
    path('ckeditor/', include('ckeditor_uploader.urls')),

    # ✅ Debug toolbar (development only)
    path('__debug__/', include('debug_toolbar.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
