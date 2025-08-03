from django.db import models
from django.conf import settings
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey
import uuid

class Course(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    
    # Course details
    difficulty = models.CharField(max_length=15, choices=DIFFICULTY_CHOICES, default='beginner')
    duration = models.IntegerField(help_text="Duration in hours", default=0)
    total_lessons = models.IntegerField(default=0)
    total_quizzes = models.IntegerField(default=0)
    
    # Pricing
    is_free = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=3, default='USD')
    
    # Media
    cover_image = models.ImageField(upload_to='course_covers/', null=True, blank=True)
    video_intro = models.URLField(blank=True, help_text="YouTube/Vimeo intro video URL")
    
    # Course settings
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    allow_enrollment = models.BooleanField(default=True)
    max_enrollments = models.IntegerField(null=True, blank=True, help_text="Maximum number of enrollments (null for unlimited)")
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_courses')
    tags = models.ManyToManyField('quizzes.Tag', blank=True, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def is_published(self):
        return self.status == 'published'

    @property
    def enrollment_count(self):
        return self.enrollments.filter(is_active=True).count()

    @property
    def average_rating(self):
        ratings = self.ratings.all()
        if ratings:
            return sum(r.rating for r in ratings) / len(ratings)
        return 0

class Lesson(MPTTModel):
    LESSON_TYPES = [
        ('video', 'Video Lesson'),
        ('text', 'Text Lesson'),
        ('interactive', 'Interactive Lesson'),
        ('quiz', 'Quiz Lesson'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    
    # Content
    content = models.TextField(blank=True, help_text="Rich text content for the lesson")
    video_url = models.URLField(blank=True, help_text="YouTube/Vimeo video URL")
    video_duration = models.IntegerField(help_text="Video duration in seconds", default=0)
    
    # Lesson type and settings
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPES, default='text')
    is_free = models.BooleanField(default=True, help_text="Free lesson (accessible without enrollment)")
    is_required = models.BooleanField(default=True, help_text="Required lesson for course completion")
    
    # Ordering
    order = models.IntegerField(default=0, help_text="Order within course")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']
        unique_together = ['course', 'order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def duration_minutes(self):
        return self.video_duration // 60 if self.video_duration else 0

class CourseEnrollment(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='course_enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    
    # Enrollment details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_active = models.BooleanField(default=True)
    
    # Progress tracking
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    completed_lessons = models.IntegerField(default=0)
    total_lessons = models.IntegerField(default=0)
    
    # Timing
    enrolled_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed = models.DateTimeField(auto_now=True)
    
    # Payment
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_currency = models.CharField(max_length=3, default='USD')
    payment_status = models.CharField(max_length=20, default='pending')

    class Meta:
        unique_together = ['user', 'course']
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"

    def calculate_progress(self):
        """Calculate and update progress percentage"""
        if self.total_lessons > 0:
            self.progress_percentage = (self.completed_lessons / self.total_lessons) * 100
        else:
            self.progress_percentage = 0
        self.save()

    def complete_enrollment(self):
        """Mark enrollment as completed"""
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.progress_percentage = 100
        self.save()

class LessonProgress(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    enrollment = models.ForeignKey(CourseEnrollment, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress')
    
    # Progress details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Video progress (for video lessons)
    video_watched_seconds = models.IntegerField(default=0)
    video_completed = models.BooleanField(default=False)
    
    # Quiz progress (for quiz lessons)
    quiz_attempts = models.IntegerField(default=0)
    best_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Timing
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['enrollment', 'lesson']
        ordering = ['lesson__order']

    def __str__(self):
        return f"{self.enrollment.user.username} - {self.lesson.title}"

    def start_lesson(self):
        """Mark lesson as started"""
        self.status = 'in_progress'
        self.started_at = timezone.now()
        self.save()

    def complete_lesson(self):
        """Mark lesson as completed"""
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.progress_percentage = 100
        self.save()

class CourseCertificate(models.Model):
    """Generate certificates for course completion"""
    enrollment = models.OneToOneField(CourseEnrollment, on_delete=models.CASCADE)
    certificate_id = models.UUIDField(default=uuid.uuid4, unique=True)
    certificate_number = models.CharField(max_length=50, unique=True)
    
    # Certificate details
    issued_at = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField(null=True, blank=True)
    is_valid = models.BooleanField(default=True)
    
    # Certificate content
    certificate_data = models.JSONField(default=dict, help_text="Store certificate template data")
    pdf_file = models.FileField(upload_to='course_certificates/', null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-issued_at']

    def __str__(self):
        return f"Certificate {self.certificate_number} - {self.enrollment.course.title}"

    def generate_certificate_number(self):
        """Generate a unique certificate number"""
        if not self.certificate_number:
            self.certificate_number = f"CERT-{self.enrollment.course.id}-{self.enrollment.user.id}-{uuid.uuid4().hex[:8].upper()}"
        return self.certificate_number

    def save(self, *args, **kwargs):
        if not self.certificate_number:
            self.generate_certificate_number()
        super().save(*args, **kwargs)

class CourseRating(models.Model):
    """User ratings for courses"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='course_ratings')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='ratings')
    
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    review = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'course']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.course.title} - {self.rating} stars" 