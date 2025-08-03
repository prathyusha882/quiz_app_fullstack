from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
import uuid

class UserAnalytics(models.Model):
    """Track user behavior and engagement"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='analytics')
    
    # Session tracking
    total_sessions = models.IntegerField(default=0)
    total_session_duration = models.DurationField(null=True, blank=True)
    last_session_at = models.DateTimeField(null=True, blank=True)
    
    # Quiz engagement
    quizzes_attempted = models.IntegerField(default=0)
    quizzes_completed = models.IntegerField(default=0)
    total_quiz_time = models.DurationField(null=True, blank=True)
    average_quiz_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Course engagement
    courses_enrolled = models.IntegerField(default=0)
    courses_completed = models.IntegerField(default=0)
    total_course_time = models.DurationField(null=True, blank=True)
    
    # Activity tracking
    last_activity = models.DateTimeField(auto_now=True)
    login_count = models.IntegerField(default=0)
    page_views = models.IntegerField(default=0)
    
    # Performance metrics
    average_response_time = models.DurationField(null=True, blank=True)
    error_count = models.IntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "User Analytics"
        ordering = ['-last_activity']

    def __str__(self):
        return f"Analytics for {self.user.username}"

    def update_session_stats(self, session_duration):
        """Update session statistics"""
        self.total_sessions += 1
        if self.total_session_duration:
            self.total_session_duration += session_duration
        else:
            self.total_session_duration = session_duration
        self.last_session_at = timezone.now()
        self.save()

    def update_quiz_stats(self, score, duration):
        """Update quiz statistics"""
        self.quizzes_attempted += 1
        if score is not None:
            current_total = self.average_quiz_score * (self.quizzes_completed or 0)
            self.quizzes_completed += 1
            self.average_quiz_score = (current_total + score) / self.quizzes_completed
        
        if self.total_quiz_time:
            self.total_quiz_time += duration
        else:
            self.total_quiz_time = duration
        self.save()

class SystemAnalytics(models.Model):
    """Track system-wide analytics and performance"""
    
    # System metrics
    total_users = models.IntegerField(default=0)
    active_users_today = models.IntegerField(default=0)
    active_users_week = models.IntegerField(default=0)
    active_users_month = models.IntegerField(default=0)
    
    # Quiz metrics
    total_quizzes = models.IntegerField(default=0)
    total_quiz_attempts = models.IntegerField(default=0)
    average_quiz_completion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Course metrics
    total_courses = models.IntegerField(default=0)
    total_course_enrollments = models.IntegerField(default=0)
    average_course_completion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Performance metrics
    average_response_time = models.DurationField(null=True, blank=True)
    error_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    uptime_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    
    # Revenue metrics (if applicable)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    monthly_recurring_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Date tracking
    date = models.DateField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "System Analytics"
        ordering = ['-date']

    def __str__(self):
        return f"System Analytics for {self.date}"

class PerformanceMetrics(models.Model):
    """Track detailed performance metrics"""
    METRIC_TYPE_CHOICES = [
        ('response_time', 'Response Time'),
        ('error_rate', 'Error Rate'),
        ('throughput', 'Throughput'),
        ('memory_usage', 'Memory Usage'),
        ('cpu_usage', 'CPU Usage'),
        ('disk_usage', 'Disk Usage'),
    ]

    # Metric details
    metric_type = models.CharField(max_length=20, choices=METRIC_TYPE_CHOICES)
    value = models.DecimalField(max_digits=10, decimal_places=4)
    unit = models.CharField(max_length=20, blank=True)
    
    # Context
    endpoint = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    
    # Timing
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['metric_type', 'timestamp']),
            models.Index(fields=['endpoint', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.metric_type}: {self.value} {self.unit} at {self.timestamp}"

class EventTracking(models.Model):
    """Track user events and actions"""
    EVENT_TYPE_CHOICES = [
        ('page_view', 'Page View'),
        ('quiz_start', 'Quiz Start'),
        ('quiz_complete', 'Quiz Complete'),
        ('course_enroll', 'Course Enrollment'),
        ('course_complete', 'Course Complete'),
        ('payment', 'Payment'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('error', 'Error'),
    ]

    # Event details
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    
    # Event context
    session_id = models.CharField(max_length=255, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    # Related objects (generic foreign key)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Event data
    event_data = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['event_type', 'timestamp']),
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['session_id', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.event_type} by {self.user.username if self.user else 'Anonymous'} at {self.timestamp}"

class ErrorLog(models.Model):
    """Track system errors and exceptions"""
    ERROR_LEVEL_CHOICES = [
        ('debug', 'Debug'),
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('critical', 'Critical'),
    ]

    # Error details
    error_level = models.CharField(max_length=10, choices=ERROR_LEVEL_CHOICES, default='error')
    error_type = models.CharField(max_length=255)
    error_message = models.TextField()
    
    # Context
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=255, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    # Stack trace and details
    stack_trace = models.TextField(blank=True)
    request_data = models.JSONField(default=dict, blank=True)
    
    # Timing
    timestamp = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    is_resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['error_level', 'timestamp']),
            models.Index(fields=['error_type', 'timestamp']),
            models.Index(fields=['is_resolved', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.error_type}: {self.error_message[:50]} at {self.timestamp}"

    def resolve_error(self):
        """Mark error as resolved"""
        self.is_resolved = True
        self.resolved_at = timezone.now()
        self.save() 