from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid

class ProctoringSession(models.Model):
    """Track proctoring sessions for quiz attempts"""
    SESSION_STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('terminated', 'Terminated'),
        ('flagged', 'Flagged for Review'),
    ]

    # Session details
    session_id = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='proctoring_sessions')
    quiz_attempt = models.OneToOneField('results.QuizAttempt', on_delete=models.CASCADE, related_name='proctoring_session')
    
    # Session status
    status = models.CharField(max_length=20, choices=SESSION_STATUS_CHOICES, default='active')
    is_valid = models.BooleanField(default=True, help_text="Mark as invalid if cheating detected")
    
    # Timing
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    last_activity = models.DateTimeField(auto_now=True)
    
    # Proctoring data
    webcam_frames = models.JSONField(default=list, help_text="Store webcam frame data")
    violation_count = models.IntegerField(default=0)
    total_risk_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    location_data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"Proctoring Session {self.session_id} - {self.user.username}"

    def end_session(self):
        """End the proctoring session"""
        self.status = 'completed'
        self.ended_at = timezone.now()
        self.save()

    def flag_for_review(self):
        """Flag session for manual review"""
        self.status = 'flagged'
        self.save()

class Violation(models.Model):
    """Track proctoring violations"""
    VIOLATION_TYPE_CHOICES = [
        ('multiple_faces', 'Multiple Faces Detected'),
        ('no_face', 'No Face Detected'),
        ('tab_switch', 'Tab Switch Detected'),
        ('fullscreen_exit', 'Fullscreen Exit'),
        ('copy_paste', 'Copy/Paste Detected'),
        ('suspicious_activity', 'Suspicious Activity'),
    ]

    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    # Violation details
    violation_id = models.UUIDField(default=uuid.uuid4, unique=True)
    proctoring_session = models.ForeignKey(ProctoringSession, on_delete=models.CASCADE, related_name='violations')
    
    # Violation information
    violation_type = models.CharField(max_length=30, choices=VIOLATION_TYPE_CHOICES)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='medium')
    description = models.TextField(blank=True)
    
    # Evidence
    evidence_data = models.JSONField(default=dict, help_text="Store evidence data")
    risk_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Timing
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Resolution
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.violation_type} - {self.proctoring_session.user.username} at {self.timestamp}"

class ProctoringSettings(models.Model):
    """Configure proctoring settings for quizzes"""
    
    # Basic settings
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    # Webcam settings
    enable_webcam = models.BooleanField(default=True)
    face_detection = models.BooleanField(default=True)
    multiple_face_detection = models.BooleanField(default=True)
    
    # Browser restrictions
    prevent_tab_switch = models.BooleanField(default=True)
    prevent_fullscreen_exit = models.BooleanField(default=True)
    prevent_copy_paste = models.BooleanField(default=True)
    
    # Risk scoring
    risk_threshold = models.DecimalField(max_digits=5, decimal_places=2, default=70.00)
    auto_terminate = models.BooleanField(default=False)
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_proctoring_settings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Proctoring Settings"
        ordering = ['name']

    def __str__(self):
        return self.name 