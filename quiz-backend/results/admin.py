# quiz-backend/results/admin.py
from django.contrib import admin
from .models import QuizAttempt, UserAnswer, Certificate, Leaderboard, QuizAnalytics

class UserAnswerInline(admin.TabularInline):
    model = UserAnswer
    extra = 0 # No extra forms by default
    readonly_fields = ('question', 'chosen_options', 'text_answer', 'is_correct_answer', 'points_earned', 'points_possible')
    can_delete = False

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'total_questions', 'correct_answers', 'incorrect_answers', 'percentage_score', 'passed', 'is_completed', 'submitted_at')
    list_filter = ('quiz', 'user', 'passed', 'is_completed', 'is_valid', 'submitted_at')
    search_fields = ('user__username', 'quiz__title')
    inlines = [UserAnswerInline]
    readonly_fields = ('user', 'quiz', 'score', 'total_questions', 'correct_answers', 'incorrect_answers', 'unanswered_questions', 'percentage_score', 'passed', 'is_completed', 'is_submitted', 'time_taken', 'time_limit_exceeded', 'violations_count', 'is_valid', 'submitted_at')
    
    # Prevent creating/editing attempts from admin, only view
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser # Only superusers can edit via admin
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser # Only superusers can delete via admin

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'is_correct_answer', 'points_earned', 'points_possible', 'is_manually_graded', 'answered_at')
    list_filter = ('is_correct_answer', 'is_manually_graded', 'question__question_type', 'answered_at')
    search_fields = ('attempt__user__username', 'question__text')
    readonly_fields = ('attempt', 'question', 'is_correct_answer', 'points_earned', 'points_possible', 'answered_at', 'time_spent')

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('certificate_number', 'attempt', 'issued_at', 'is_valid')
    list_filter = ('is_valid', 'issued_at')
    search_fields = ('certificate_number', 'attempt__user__username', 'attempt__quiz__title')
    readonly_fields = ('certificate_id', 'certificate_number', 'attempt', 'issued_at', 'pdf_file')

@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'user', 'rank', 'score', 'percentage_score', 'time_taken')
    list_filter = ('quiz', 'rank')
    search_fields = ('user__username', 'quiz__title')
    readonly_fields = ('quiz', 'user', 'attempt', 'score', 'percentage_score', 'time_taken', 'rank', 'created_at')

@admin.register(QuizAnalytics)
class QuizAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'total_attempts', 'total_participants', 'average_score', 'pass_rate', 'last_updated')
    list_filter = ('last_updated',)
    search_fields = ('quiz__title',)
    readonly_fields = ('quiz', 'total_attempts', 'total_participants', 'average_score', 'average_time', 'pass_rate', 'question_analytics', 'daily_stats', 'weekly_stats', 'last_updated')