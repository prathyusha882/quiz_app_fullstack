from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    # User analytics
    path('user/', views.UserAnalyticsView.as_view(), name='user-analytics'),
    path('user/events/', views.UserEventsView.as_view(), name='user-events'),
    
    # System analytics
    path('system/', views.SystemAnalyticsView.as_view(), name='system-analytics'),
    path('system/performance/', views.PerformanceMetricsView.as_view(), name='performance-metrics'),
    path('system/errors/', views.ErrorLogView.as_view(), name='error-logs'),
    
    # Quiz analytics
    path('quizzes/', views.QuizAnalyticsView.as_view(), name='quiz-analytics'),
    path('quizzes/<int:quiz_id>/', views.QuizDetailAnalyticsView.as_view(), name='quiz-detail-analytics'),
    
    # Course analytics
    path('courses/', views.CourseAnalyticsView.as_view(), name='course-analytics'),
    path('courses/<int:course_id>/', views.CourseDetailAnalyticsView.as_view(), name='course-detail-analytics'),
    
    # Event tracking
    path('events/track/', views.EventTrackingView.as_view(), name='track-event'),
    
    # Reports
    path('reports/', views.AnalyticsReportsView.as_view(), name='analytics-reports'),
    path('reports/export/', views.ExportAnalyticsView.as_view(), name='export-analytics'),
] 