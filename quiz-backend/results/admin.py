# quiz-backend/results/admin.py
from django.contrib import admin
from .models import QuizAttempt, UserAnswer

class UserAnswerInline(admin.TabularInline):
    model = UserAnswer
    extra = 0 # No extra forms by default
    readonly_fields = ('question', 'chosen_option', 'chosen_text_answer', 'is_correct_answer')
    can_delete = False

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'total_questions', 'passed', 'time_taken', 'submitted_at')
    list_filter = ('quiz', 'user', 'passed', 'submitted_at')
    search_fields = ('user__username', 'quiz__title')
    inlines = [UserAnswerInline]
    readonly_fields = ('user', 'quiz', 'score', 'total_questions', 'passed', 'time_taken', 'submitted_at')
    # Prevent creating/editing attempts from admin, only view
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser # Only superusers can edit via admin
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser # Only superusers can delete via admin