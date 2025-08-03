# quiz-backend/quizzes/serializers.py
from rest_framework import serializers
from .models import Quiz, Question, Option, Tag, QuizSession
from django.utils import timezone
import uuid

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'created_at']

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'is_correct', 'order', 'explanation']

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'points', 'explanation', 
                 'image', 'image_url', 'is_required', 'order', 'options', 
                 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_image_url(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

class QuestionCreateSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)
    
    class Meta:
        model = Question
        fields = ['text', 'question_type', 'points', 'explanation', 
                 'image', 'is_required', 'order', 'options']
    
    def create(self, validated_data):
        options_data = validated_data.pop('options', [])
        question = Question.objects.create(**validated_data)
        
        for option_data in options_data:
            Option.objects.create(question=question, **option_data)
        
        return question
    
    def update(self, instance, validated_data):
        options_data = validated_data.pop('options', [])
        
        # Update question fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update options
        instance.options.all().delete()
        for option_data in options_data:
            Option.objects.create(question=instance, **option_data)
        
        return instance

class QuizListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    created_by = serializers.StringRelatedField()
    cover_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'slug', 'description', 'difficulty', 
                 'duration', 'time_limit', 'passing_score', 'max_attempts',
                 'is_active', 'status', 'tags', 'created_by', 'cover_image_url',
                 'question_count', 'total_points', 'created_at', 'updated_at']
        read_only_fields = ['slug', 'question_count', 'total_points', 'created_at', 'updated_at']
    
    def get_cover_image_url(self, obj):
        if obj.cover_image:
            return self.context['request'].build_absolute_uri(obj.cover_image.url)
        return None

class QuizDetailSerializer(QuizListSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    instructions_file_url = serializers.SerializerMethodField()
    
    class Meta(QuizListSerializer.Meta):
        fields = QuizListSerializer.Meta.fields + ['questions', 'instructions_file_url']
    
    def get_instructions_file_url(self, obj):
        if obj.instructions_file:
            return self.context['request'].build_absolute_uri(obj.instructions_file.url)
        return None

class QuizCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all(), required=False)
    
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'difficulty', 'duration', 'time_limit',
                 'passing_score', 'max_attempts', 'is_active', 'status',
                 'allow_backtracking', 'shuffle_questions', 'show_correct_answers',
                 'require_fullscreen', 'enable_proctoring', 'cover_image',
                 'instructions_file', 'tags']
    
    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        validated_data['created_by'] = self.context['request'].user
        quiz = Quiz.objects.create(**validated_data)
        quiz.tags.set(tags)
        return quiz

class QuizUpdateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all(), required=False)
    
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'difficulty', 'duration', 'time_limit',
                 'passing_score', 'max_attempts', 'is_active', 'status',
                 'allow_backtracking', 'shuffle_questions', 'show_correct_answers',
                 'require_fullscreen', 'enable_proctoring', 'cover_image',
                 'instructions_file', 'tags']
    
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        
        # Handle file uploads
        if 'cover_image' in validated_data and validated_data['cover_image'] is None:
            if instance.cover_image:
                instance.cover_image.delete(save=False)
        
        if 'instructions_file' in validated_data and validated_data['instructions_file'] is None:
            if instance.instructions_file:
                instance.instructions_file.delete(save=False)
        
        # Update fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update tags
        if tags is not None:
            instance.tags.set(tags)
        
        return instance

class QuizSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizSession
        fields = ['id', 'session_id', 'started_at', 'last_activity', 
                 'is_active', 'current_question', 'answers_saved', 'violations']
        read_only_fields = ['session_id', 'started_at', 'last_activity', 'violations']
    
    def create(self, validated_data):
        validated_data['session_id'] = uuid.uuid4()
        return super().create(validated_data)

class QuizAttemptSerializer(serializers.ModelSerializer):
    quiz = QuizListSerializer(read_only=True)
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Quiz
        fields = ['id', 'quiz', 'user', 'score', 'total_questions', 
                 'correct_answers', 'incorrect_answers', 'unanswered_questions',
                 'percentage_score', 'passed', 'is_completed', 'is_submitted',
                 'started_at', 'submitted_at', 'time_taken', 'time_limit_exceeded',
                 'violations_count', 'is_valid']
        read_only_fields = ['id', 'quiz', 'user', 'score', 'total_questions',
                           'correct_answers', 'incorrect_answers', 'unanswered_questions',
                           'percentage_score', 'passed', 'is_completed', 'is_submitted',
                           'started_at', 'submitted_at', 'time_taken', 'time_limit_exceeded',
                           'violations_count', 'is_valid']

class QuizAnalyticsSerializer(serializers.Serializer):
    total_attempts = serializers.IntegerField()
    total_participants = serializers.IntegerField()
    average_score = serializers.DecimalField(max_digits=5, decimal_places=2)
    average_time = serializers.DurationField()
    pass_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    question_analytics = serializers.DictField()
    daily_stats = serializers.DictField()
    weekly_stats = serializers.DictField()

class QuizFilterSerializer(serializers.Serializer):
    difficulty = serializers.ChoiceField(choices=Quiz.DIFFICULTY_CHOICES, required=False)
    tags = serializers.ListField(child=serializers.IntegerField(), required=False)
    status = serializers.ChoiceField(choices=Quiz.STATUS_CHOICES, required=False)
    created_by = serializers.IntegerField(required=False)
    search = serializers.CharField(required=False)
    is_active = serializers.BooleanField(required=False)

class QuestionBankSerializer(serializers.ModelSerializer):
    quiz_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'points', 'explanation',
                 'image', 'is_required', 'order', 'created_at', 'updated_at', 'quiz_count']
        read_only_fields = ['created_at', 'updated_at', 'quiz_count']
    
    def get_quiz_count(self, obj):
        return obj.quiz_set.count()

class QuestionImportSerializer(serializers.Serializer):
    file = serializers.FileField()
    quiz_id = serializers.IntegerField()
    overwrite = serializers.BooleanField(default=False)
    
    def validate_file(self, value):
        if not value.name.endswith(('.csv', '.xlsx', '.xls')):
            raise serializers.ValidationError("File must be CSV or Excel format")
        return value

class QuizExportSerializer(serializers.Serializer):
    quiz_id = serializers.IntegerField()
    format = serializers.ChoiceField(choices=['pdf', 'csv', 'json'], default='pdf')
    include_answers = serializers.BooleanField(default=False)
    include_analytics = serializers.BooleanField(default=False)