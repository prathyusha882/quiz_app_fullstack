from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.conf import settings

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default='#3B82F6')  # Hex color code
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Quiz(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    duration = models.IntegerField(help_text="Duration in minutes", default=30)
    time_limit = models.IntegerField(help_text="Time limit in minutes", default=30)
    passing_score = models.IntegerField(default=70, help_text="Minimum score to pass (percentage)")
    max_attempts = models.IntegerField(default=1, help_text="Maximum attempts allowed per user")
    is_active = models.BooleanField(default=True)
    allow_backtracking = models.BooleanField(default=False, help_text="Allow users to go back to previous questions")
    shuffle_questions = models.BooleanField(default=False, help_text="Randomize question order")
    show_correct_answers = models.BooleanField(default=True, help_text="Show correct answers after submission")
    require_fullscreen = models.BooleanField(default=False, help_text="Require fullscreen mode during quiz")
    enable_proctoring = models.BooleanField(default=False, help_text="Enable basic proctoring features")
    
    # File uploads
    cover_image = models.ImageField(upload_to='quiz_covers/', null=True, blank=True)
    instructions_file = models.FileField(upload_to='quiz_instructions/', null=True, blank=True)
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_quizzes')
    tags = models.ManyToManyField(Tag, blank=True, related_name='quizzes')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Quizzes"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def question_count(self):
        return self.questions.count()

    @property
    def total_points(self):
        return sum(question.points for question in self.questions.all())

    @property
    def is_published(self):
        return self.status == 'published' and self.is_active

    def get_user_attempts(self, user):
        """Get all attempts by a specific user for this quiz"""
        return self.attempts.filter(user=user)

    def can_user_attempt(self, user):
        """Check if user can attempt this quiz"""
        if not self.is_published:
            return False, "Quiz is not available"
        
        user_attempts = self.get_user_attempts(user)
        if user_attempts.count() >= self.max_attempts:
            return False, f"Maximum attempts ({self.max_attempts}) reached"
        
        return True, "Can attempt"

class Question(models.Model):
    QUESTION_TYPES = [
        ('multiple-choice', 'Multiple Choice'),
        ('checkbox', 'Checkbox (Multiple Answers)'),
        ('text-input', 'Text Input (Short Answer)'),
        ('essay', 'Essay (Long Answer)'),
        ('file-upload', 'File Upload'),
    ]

    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='multiple-choice')
    points = models.IntegerField(default=1, help_text="Points awarded for correct answer")
    explanation = models.TextField(blank=True, help_text="Explanation shown after answering")
    image = models.ImageField(upload_to='question_images/', null=True, blank=True)
    is_required = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Question order in quiz")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']
        unique_together = ['quiz', 'order']

    def __str__(self):
         return f"Q: {self.text[:50]}... (Quiz: {self.quiz.title if self.quiz else 'No Quiz'})"

    @property
    def correct_options(self):
        """Get all correct options for this question"""
        return self.options.filter(is_correct=True)

    @property
    def has_multiple_correct_answers(self):
        """Check if question has multiple correct answers"""
        return self.correct_options.count() > 1

class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0, help_text="Option order")
    explanation = models.TextField(blank=True, help_text="Explanation for this option")

    class Meta:
        unique_together = ('question', 'text')
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.text} ({'Correct' if self.is_correct else 'Incorrect'})"

class QuizSession(models.Model):
    """Track active quiz sessions for anti-cheating features"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    session_id = models.UUIDField(unique=True)
    started_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    current_question = models.IntegerField(default=1)
    answers_saved = models.JSONField(default=dict, help_text="Store answers as user progresses")
    violations = models.JSONField(default=list, help_text="Track cheating violations")
    
    class Meta:
        unique_together = ['user', 'quiz', 'session_id']
    
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} (Session: {self.session_id})"
    
    def add_violation(self, violation_type, details=""):
        """Add a cheating violation"""
        self.violations.append({
            'type': violation_type,
            'details': details,
            'timestamp': timezone.now().isoformat()
        })
        self.save()
    
    def is_violation_free(self):
        """Check if session has no violations"""
        return len(self.violations) == 0
