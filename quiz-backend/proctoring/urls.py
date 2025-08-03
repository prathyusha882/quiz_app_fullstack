from django.urls import path
from . import views

app_name = 'proctoring'

urlpatterns = [
    # Proctoring sessions
    path('session/start/', views.StartProctoringSessionView.as_view(), name='start-session'),
    path('session/<uuid:session_id>/', views.ProctoringSessionView.as_view(), name='session-detail'),
    path('session/<uuid:session_id>/end/', views.EndProctoringSessionView.as_view(), name='end-session'),
    
    # Violations
    path('violations/', views.ViolationListView.as_view(), name='violation-list'),
    path('violations/<uuid:violation_id>/', views.ViolationDetailView.as_view(), name='violation-detail'),
    path('violations/<uuid:violation_id>/resolve/', views.ResolveViolationView.as_view(), name='resolve-violation'),
    
    # Settings
    path('settings/', views.ProctoringSettingsListView.as_view(), name='settings-list'),
    path('settings/create/', views.ProctoringSettingsCreateView.as_view(), name='settings-create'),
    path('settings/<int:settings_id>/', views.ProctoringSettingsDetailView.as_view(), name='settings-detail'),
    path('settings/<int:settings_id>/edit/', views.ProctoringSettingsUpdateView.as_view(), name='settings-update'),
    
    # Reports
    path('reports/', views.ProctoringReportsView.as_view(), name='reports'),
    path('reports/<uuid:session_id>/', views.ProctoringReportDetailView.as_view(), name='report-detail'),
] 