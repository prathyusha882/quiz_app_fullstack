from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # Course management
    path('', views.CourseListView.as_view(), name='course-list'),
    path('create/', views.CourseCreateView.as_view(), name='course-create'),
    path('<slug:slug>/', views.CourseDetailView.as_view(), name='course-detail'),
    path('<slug:slug>/edit/', views.CourseUpdateView.as_view(), name='course-update'),
    path('<slug:slug>/delete/', views.CourseDeleteView.as_view(), name='course-delete'),
    
    # Lesson management
    path('<slug:course_slug>/lessons/', views.LessonListView.as_view(), name='lesson-list'),
    path('<slug:course_slug>/lessons/create/', views.LessonCreateView.as_view(), name='lesson-create'),
    path('<slug:course_slug>/lessons/<slug:lesson_slug>/', views.LessonDetailView.as_view(), name='lesson-detail'),
    path('<slug:course_slug>/lessons/<slug:lesson_slug>/edit/', views.LessonUpdateView.as_view(), name='lesson-update'),
    
    # Enrollment
    path('<slug:slug>/enroll/', views.CourseEnrollView.as_view(), name='course-enroll'),
    path('<slug:slug>/unenroll/', views.CourseUnenrollView.as_view(), name='course-unenroll'),
    path('my-courses/', views.UserCourseListView.as_view(), name='user-course-list'),
    
    # Progress
    path('<slug:course_slug>/progress/', views.CourseProgressView.as_view(), name='course-progress'),
    path('<slug:course_slug>/lessons/<slug:lesson_slug>/progress/', views.LessonProgressView.as_view(), name='lesson-progress'),
    
    # Certificates
    path('<slug:slug>/certificate/', views.CourseCertificateView.as_view(), name='course-certificate'),
    
    # Ratings and Reviews
    path('<slug:slug>/rate/', views.CourseRatingView.as_view(), name='course-rate'),
    path('<slug:slug>/reviews/', views.CourseReviewsView.as_view(), name='course-reviews'),
] 