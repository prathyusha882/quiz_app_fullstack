# quiz-backend/results/models.py
from django.db import models
from django.conf import settings
from quizzes.models import Quiz, Question, Option # Import models from quizzes app

class QuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='quiz_attempts', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name='attempts', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    passed = models.BooleanField(default=False) # Based on a passing score (e.g., 70%)
    time_taken = models.CharField(max_length=20, blank=True, null=True, help_text="e.g., '05:30'") # Time taken to complete
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']
        # You might want to add a unique_together constraint for user and quiz if a user can only attempt a quiz once
        # Or, if multiple attempts are allowed, ensure the `submitted_at` field is precise enough for unique identification.
        # unique_together = ('user', 'quiz', 'submitted_at') # If you want to track each specific attempt uniquely

    def __str__(self):
        return f"{self.user.username}'s attempt on {self.quiz.title} (Score: {self.score}/{self.total_questions})"

class UserAnswer(models.Model):
    attempt = models.ForeignKey(QuizAttempt, related_name='user_answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # Store chosen option for multiple-choice/checkbox
    chosen_option = models.ForeignKey(Option, null=True, blank=True, on_delete=models.SET_NULL)
    # Store chosen text for text-input questions
    chosen_text_answer = models.TextField(blank=True, null=True)
    is_correct_answer = models.BooleanField(default=False)

    class Meta:
        unique_together = ('attempt', 'question') # A user can only answer a question once per attempt
        ordering = ['question__id'] # Order answers by question ID for consistency

    def __str__(self):
        return f"Attempt {self.attempt.id} - Q: {self.question.id} - Correct: {self.is_correct_answer}"