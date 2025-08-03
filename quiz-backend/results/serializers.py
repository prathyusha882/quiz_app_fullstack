# quiz-backend/results/serializers.py
from rest_framework import serializers
from .models import QuizAttempt, UserAnswer, Certificate, Leaderboard, QuizAnalytics
from quizzes.models import Quiz, Question, Option
from django.utils import timezone

class UserAnswerSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    chosen_options = serializers.PrimaryKeyRelatedField(many=True, queryset=Option.objects.all(), required=False)
    
    class Meta:
        model = UserAnswer
        fields = ['id', 'question', 'chosen_options', 'text_answer', 'uploaded_file',
                 'is_correct_answer', 'points_earned', 'points_possible', 'answered_at',
                 'time_spent', 'is_manually_graded', 'manual_score', 'graded_by', 'graded_at',
                 'grading_notes']
        read_only_fields = ['id', 'is_correct_answer', 'points_earned', 'points_possible',
                           'answered_at', 'is_manually_graded', 'graded_by', 'graded_at']

class QuizAttemptSerializer(serializers.ModelSerializer):
    user_answers = UserAnswerSerializer(many=True, read_only=True)
    quiz_title = serializers.CharField(source='quiz.title', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = QuizAttempt
        fields = ['id', 'user', 'quiz', 'quiz_title', 'user_name', 'session',
                 'score', 'total_questions', 'correct_answers', 'incorrect_answers',
                 'unanswered_questions', 'percentage_score', 'passed', 'is_completed',
                 'is_submitted', 'started_at', 'submitted_at', 'time_taken',
                 'time_limit_exceeded', 'violations_count', 'is_valid', 'ip_address',
                 'user_agent', 'browser_info', 'user_answers']
        read_only_fields = ['id', 'quiz_title', 'user_name', 'score', 'total_questions',
                           'correct_answers', 'incorrect_answers', 'unanswered_questions',
                           'percentage_score', 'passed', 'is_completed', 'is_submitted',
                           'started_at', 'submitted_at', 'time_taken', 'time_limit_exceeded',
                           'violations_count', 'is_valid', 'ip_address', 'user_agent',
                           'browser_info']

class QuizAttemptCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = ['quiz', 'session']
        read_only_fields = ['user']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class QuizAttemptSubmitSerializer(serializers.Serializer):
    answers = serializers.ListField(
        child=serializers.DictField()
    )
    
    def validate_answers(self, value):
        for answer in value:
            if 'question' not in answer:
                raise serializers.ValidationError("Each answer must include a question ID")
        return value

class CertificateSerializer(serializers.ModelSerializer):
    attempt = QuizAttemptSerializer(read_only=True)
    pdf_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Certificate
        fields = ['id', 'attempt', 'certificate_id', 'certificate_number',
                 'issued_at', 'valid_until', 'is_valid', 'certificate_data', 'pdf_file', 'pdf_url']
        read_only_fields = ['certificate_id', 'certificate_number', 'issued_at', 'pdf_file']
    
    def get_pdf_url(self, obj):
        if obj.pdf_file:
            return self.context['request'].build_absolute_uri(obj.pdf_file.url)
        return None

class CertificateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ['attempt']
    
    def create(self, validated_data):
        from .services import CertificateService
        attempt = validated_data['attempt']
        certificate = CertificateService.generate_certificate(attempt)
        return certificate

class LeaderboardSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_full_name = serializers.SerializerMethodField()
    quiz_title = serializers.CharField(source='quiz.title', read_only=True)
    
    class Meta:
        model = Leaderboard
        fields = ['id', 'quiz', 'quiz_title', 'user', 'user_name', 'user_full_name',
                 'attempt', 'score', 'percentage_score', 'time_taken', 'rank', 'created_at']
        read_only_fields = ['id', 'quiz_title', 'user_name', 'user_full_name', 'rank', 'created_at']
    
    def get_user_full_name(self, obj):
        if obj.user.first_name and obj.user.last_name:
            return f"{obj.user.first_name} {obj.user.last_name}"
        return obj.user.username

class QuizAnalyticsSerializer(serializers.ModelSerializer):
    quiz_title = serializers.CharField(source='quiz.title', read_only=True)
    
    class Meta:
        model = QuizAnalytics
        fields = ['id', 'quiz', 'quiz_title', 'total_attempts', 'total_participants',
                 'average_score', 'average_time', 'pass_rate', 'question_analytics',
                 'daily_stats', 'weekly_stats', 'last_updated']
        read_only_fields = ['id', 'quiz_title', 'total_attempts', 'total_participants',
                           'average_score', 'average_time', 'pass_rate', 'question_analytics',
                           'daily_stats', 'weekly_stats', 'last_updated']

class ManualGradingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = ['manual_score', 'grading_notes']
    
    def update(self, instance, validated_data):
        instance.manual_score = validated_data.get('manual_score', instance.manual_score)
        instance.grading_notes = validated_data.get('grading_notes', instance.grading_notes)
        instance.graded_by = self.context['request'].user
        instance.graded_at = timezone.now()
        instance.is_manually_graded = True
        instance.save()
        
        # Recalculate attempt score
        attempt = instance.attempt
        attempt.calculate_score()
        
        return instance

class ProgressTrackingSerializer(serializers.Serializer):
    total_quizzes_taken = serializers.IntegerField()
    total_score = serializers.IntegerField()
    average_score = serializers.DecimalField(max_digits=5, decimal_places=2)
    certificates_earned = serializers.IntegerField()
    quizzes_passed = serializers.IntegerField()
    total_time_spent = serializers.DurationField()
    recent_attempts = serializers.ListField()
    performance_by_difficulty = serializers.DictField()
    performance_by_tag = serializers.DictField()

class UserStatsSerializer(serializers.Serializer):
    total_attempts = serializers.IntegerField()
    total_quizzes = serializers.IntegerField()
    average_score = serializers.DecimalField(max_digits=5, decimal_places=2)
    best_score = serializers.DecimalField(max_digits=5, decimal_places=2)
    total_time_spent = serializers.DurationField()
    certificates_earned = serializers.IntegerField()
    quizzes_passed = serializers.IntegerField()
    current_streak = serializers.IntegerField()
    longest_streak = serializers.IntegerField()

class QuizResultSummarySerializer(serializers.Serializer):
    quiz_id = serializers.IntegerField()
    quiz_title = serializers.CharField()
    total_questions = serializers.IntegerField()
    correct_answers = serializers.IntegerField()
    incorrect_answers = serializers.IntegerField()
    unanswered_questions = serializers.IntegerField()
    score = serializers.IntegerField()
    percentage_score = serializers.DecimalField(max_digits=5, decimal_places=2)
    passed = serializers.BooleanField()
    time_taken = serializers.DurationField()
    time_limit_exceeded = serializers.BooleanField()
    violations_count = serializers.IntegerField()
    is_valid = serializers.BooleanField()
    submitted_at = serializers.DateTimeField()

class AnswerReviewSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.text', read_only=True)
    question_type = serializers.CharField(source='question.question_type', read_only=True)
    correct_options = serializers.SerializerMethodField()
    chosen_options_text = serializers.SerializerMethodField()
    
    class Meta:
        model = UserAnswer
        fields = ['id', 'question', 'question_text', 'question_type', 'chosen_options',
                 'chosen_options_text', 'text_answer', 'uploaded_file', 'is_correct_answer',
                 'points_earned', 'points_possible', 'answered_at', 'time_spent',
                 'is_manually_graded', 'manual_score', 'grading_notes', 'correct_options']
        read_only_fields = ['id', 'question_text', 'question_type', 'is_correct_answer',
                           'points_earned', 'points_possible', 'answered_at', 'time_spent',
                           'is_manually_graded', 'manual_score', 'grading_notes']
    
    def get_correct_options(self, obj):
        if obj.question.question_type in ['multiple-choice', 'checkbox']:
            return [{'id': opt.id, 'text': opt.text} for opt in obj.question.correct_options]
        return []
    
    def get_chosen_options_text(self, obj):
        return [opt.text for opt in obj.chosen_options.all()]

class ExportResultsSerializer(serializers.Serializer):
    quiz_id = serializers.IntegerField()
    format = serializers.ChoiceField(choices=['pdf', 'csv', 'json'], default='pdf')
    include_answers = serializers.BooleanField(default=True)
    include_analytics = serializers.BooleanField(default=False)
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False) 