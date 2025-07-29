# quiz-backend/quizzes/admin.py
from django.contrib import admin
from .models import Quiz, Question, Option

# Inline for Options within Question admin
class OptionInline(admin.TabularInline):
    model = Option
    extra = 3 # Number of empty forms to display

# Inline for Questions within Quiz admin
class QuestionInline(admin.TabularInline):
    model = Question
    inlines = [OptionInline] # Allow adding options directly in Question inline
    extra = 1 # Number of empty forms to display

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'duration', 'is_active', 'created_at', 'updated_at')
    list_filter = ('difficulty', 'is_active')
    search_fields = ('title', 'description')
    inlines = [QuestionInline] # Add Question inline to Quiz admin
    prepopulated_fields = {'slug': ('title',)} # Auto-fill slug from title (optional)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'text', 'question_type')
    list_filter = ('quiz', 'question_type')
    search_fields = ('text',)
    inlines = [OptionInline] # Add Option inline to Question admin

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'is_correct')
    list_filter = ('question', 'is_correct')
    search_fields = ('text',)