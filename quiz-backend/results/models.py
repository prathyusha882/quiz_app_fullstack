# quiz-backend/results/models.py
from django.db import models
from django.conf import settings
from quizzes.models import Quiz, Question, Option, QuizSession
from django.utils import timezone
import uuid

class QuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='quiz_attempts', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name='attempts', on_delete=models.CASCADE)
    session = models.OneToOneField(QuizSession, on_delete=models.CASCADE, null=True, blank=True)
    
    # Scoring
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    incorrect_answers = models.IntegerField(default=0)
    unanswered_questions = models.IntegerField(default=0)
    percentage_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Status
    passed = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    is_submitted = models.BooleanField(default=False)
    
    # Timing
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    time_taken = models.DurationField(null=True, blank=True)
    time_limit_exceeded = models.BooleanField(default=False)
    
    # Anti-cheating
    violations_count = models.IntegerField(default=0)
    is_valid = models.BooleanField(default=True, help_text="Mark as invalid if cheating detected")
    
    # Metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    browser_info = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-submitted_at']
        unique_together = ['user', 'quiz', 'started_at']

    def __str__(self):
        return f"{self.user.username}'s attempt on {self.quiz.title} (Score: {self.score}/{self.total_questions})"
    
    def calculate_score(self):
        """Calculate and update the score"""
        correct_answers = self.user_answers.filter(is_correct_answer=True).count()
        total_questions = self.user_answers.count()
        
        self.correct_answers = correct_answers
        self.incorrect_answers = total_questions - correct_answers
        self.total_questions = total_questions
        
        if total_questions > 0:
            self.percentage_score = (correct_answers / total_questions) * 100
            self.passed = self.percentage_score >= self.quiz.passing_score
        else:
            self.percentage_score = 0
            self.passed = False
        
        self.score = correct_answers
        self.save()
    
    def complete_attempt(self):
        """Mark attempt as completed"""
        self.is_completed = True
        self.submitted_at = timezone.now()
        if self.started_at:
            self.time_taken = self.submitted_at - self.started_at
        self.calculate_score()
        self.save()

class UserAnswer(models.Model):
    attempt = models.ForeignKey(QuizAttempt, related_name='user_answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    # Multiple choice/checkbox answers
    chosen_options = models.ManyToManyField(Option, blank=True, related_name='user_answers')
    
    # Text-based answers
    text_answer = models.TextField(blank=True, null=True)
    
    # File upload answers
    uploaded_file = models.FileField(upload_to='user_uploads/', null=True, blank=True)
    
    # Scoring
    is_correct_answer = models.BooleanField(default=False)
    points_earned = models.IntegerField(default=0)
    points_possible = models.IntegerField(default=0)
    
    # Timing
    answered_at = models.DateTimeField(auto_now_add=True)
    time_spent = models.DurationField(null=True, blank=True)
    
    # Manual grading (for subjective questions)
    is_manually_graded = models.BooleanField(default=False)
    manual_score = models.IntegerField(null=True, blank=True)
    graded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    graded_at = models.DateTimeField(null=True, blank=True)
    grading_notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('attempt', 'question')
        ordering = ['question__order']

    def __str__(self):
        return f"Attempt {self.attempt.id} - Q: {self.question.id} - Correct: {self.is_correct_answer}"
    
    def grade_answer(self):
        """Grade the answer based on question type"""
        if self.question.question_type == 'multiple-choice':
            self._grade_multiple_choice()
        elif self.question.question_type == 'checkbox':
            self._grade_checkbox()
        elif self.question.question_type in ['text-input', 'essay']:
            # These require manual grading
            self.is_manually_graded = True
            self.points_possible = self.question.points
        elif self.question.question_type == 'file-upload':
            # File uploads require manual grading
            self.is_manually_graded = True
            self.points_possible = self.question.points
        
        self.save()
    
    def _grade_multiple_choice(self):
        """Grade multiple choice questions"""
        correct_options = self.question.correct_options
        chosen_options = self.chosen_options.all()
        
        # Check if all correct options are chosen and no incorrect ones
        correct_chosen = all(option in chosen_options for option in correct_options)
        incorrect_chosen = any(option not in correct_options for option in chosen_options)
        
        self.is_correct_answer = correct_chosen and not incorrect_chosen
        self.points_possible = self.question.points
        self.points_earned = self.question.points if self.is_correct_answer else 0
        self.is_manually_graded = False
    
    def _grade_checkbox(self):
        """Grade checkbox questions"""
        correct_options = set(self.question.correct_options)
        chosen_options = set(self.chosen_options.all())
        
        # Partial credit for partially correct answers
        correct_chosen = len(correct_options.intersection(chosen_options))
        incorrect_chosen = len(chosen_options - correct_options)
        
        if incorrect_chosen == 0 and correct_chosen == len(correct_options):
            # Perfect answer
            self.is_correct_answer = True
            self.points_earned = self.question.points
        elif incorrect_chosen == 0 and correct_chosen > 0:
            # Partial credit
            self.is_correct_answer = False
            self.points_earned = int((correct_chosen / len(correct_options)) * self.question.points)
        else:
            # Wrong answer
            self.is_correct_answer = False
            self.points_earned = 0
        
        self.points_possible = self.question.points
        self.is_manually_graded = False

class Certificate(models.Model):
    """Generate certificates for quiz completion"""
    attempt = models.OneToOneField(QuizAttempt, on_delete=models.CASCADE)
    certificate_id = models.UUIDField(default=uuid.uuid4, unique=True)
    certificate_number = models.CharField(max_length=50, unique=True)
    
    # Certificate details
    issued_at = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField(null=True, blank=True)
    is_valid = models.BooleanField(default=True)
    
    # Certificate content
    certificate_data = models.JSONField(default=dict, help_text="Store certificate template data")
    pdf_file = models.FileField(upload_to='certificates/', null=True, blank=True)
    
    class Meta:
        ordering = ['-issued_at']
    
    def __str__(self):
        return f"Certificate {self.certificate_number} - {self.attempt.user.username}"
    
    def generate_certificate_number(self):
        """Generate a unique certificate number"""
        import datetime
        date_str = datetime.datetime.now().strftime('%Y%m%d')
        count = Certificate.objects.filter(issued_at__date=datetime.datetime.now().date()).count() + 1
        return f"CERT-{date_str}-{count:04d}"
    
    def save(self, *args, **kwargs):
        if not self.certificate_number:
            self.certificate_number = self.generate_certificate_number()
        super().save(*args, **kwargs)

class Leaderboard(models.Model):
    """Global leaderboard for quiz performance"""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='leaderboard_entries')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    attempt = models.OneToOneField(QuizAttempt, on_delete=models.CASCADE)
    
    # Performance metrics
    score = models.IntegerField()
    percentage_score = models.DecimalField(max_digits=5, decimal_places=2)
    time_taken = models.DurationField()
    rank = models.IntegerField()
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['rank', 'time_taken']
        unique_together = ['quiz', 'user', 'attempt']
    
    def __str__(self):
        return f"{self.user.username} - Rank {self.rank} - {self.quiz.title}"

class QuizAnalytics(models.Model):
    """Analytics for quiz performance"""
    quiz = models.OneToOneField(Quiz, on_delete=models.CASCADE)
    
    # Statistics
    total_attempts = models.IntegerField(default=0)
    total_participants = models.IntegerField(default=0)
    average_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    average_time = models.DurationField(null=True, blank=True)
    pass_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Question analytics
    question_analytics = models.JSONField(default=dict, help_text="Store per-question statistics")
    
    # Time-based analytics
    daily_stats = models.JSONField(default=dict, help_text="Daily participation statistics")
    weekly_stats = models.JSONField(default=dict, help_text="Weekly participation statistics")
    
    # Last updated
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Quiz Analytics"
    
    def __str__(self):
        return f"Analytics for {self.quiz.title}"
    
    def update_analytics(self):
        """Update analytics based on current attempts"""
        attempts = self.quiz.attempts.filter(is_completed=True)
        
        self.total_attempts = attempts.count()
        self.total_participants = attempts.values('user').distinct().count()
        
        if self.total_attempts > 0:
            scores = [attempt.percentage_score for attempt in attempts]
            self.average_score = sum(scores) / len(scores)
            
            passed_attempts = attempts.filter(passed=True).count()
            self.pass_rate = (passed_attempts / self.total_attempts) * 100
            
            # Calculate average time
            times = [attempt.time_taken for attempt in attempts if attempt.time_taken]
            if times:
                total_seconds = sum(t.total_seconds() for t in times)
                avg_seconds = total_seconds / len(times)
                self.average_time = timezone.timedelta(seconds=avg_seconds)
        
        self.save()