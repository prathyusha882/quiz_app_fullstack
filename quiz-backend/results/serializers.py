# quiz-backend/results/serializers.py
from rest_framework import serializers
from .models import QuizAttempt, UserAnswer
from quizzes.models import Quiz, Question, Option
from quizzes.serializers import QuestionSerializer, OptionSerializer # Re-use QuestionSerializer for review


class UserAnswerSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(read_only=True) # Read-only, question object is linked via views
    # Optionally, to display question details in the result review:
    # question_details = QuestionSerializer(source='question', read_only=True)

    class Meta:
        model = UserAnswer
        fields = ['question', 'chosen_option', 'chosen_text_answer', 'is_correct_answer']


class QuizAttemptSerializer(serializers.ModelSerializer):
    user_answers = UserAnswerSerializer(many=True, read_only=True) # Nested answers for review
    quiz_title = serializers.ReadOnlyField(source='quiz.title') # Read quiz title directly
    username = serializers.ReadOnlyField(source='user.username') # Read username directly

    class Meta:
        model = QuizAttempt
        fields = [
            'id', 'user', 'username', 'quiz', 'quiz_title', 'score', 'total_questions',
            'passed', 'time_taken', 'submitted_at', 'user_answers'
        ]
        read_only_fields = [
            'id', 'user', 'username', 'quiz', 'quiz_title', 'score', 'total_questions',
            'passed', 'time_taken', 'submitted_at', 'user_answers'
        ]


class QuizSubmissionSerializer(serializers.Serializer):
    """
    Serializer for handling quiz submission data from the frontend.
    It takes question_id and submitted_answer (can be string or list of strings for checkboxes).
    """
    question_id = serializers.CharField(max_length=255)
    submitted_answer = serializers.JSONField() # Can be string, list of strings, etc.
    # Frontend also passes `timeTaken` (e.g., '05:30'), but we'll add it directly to QuizAttempt creation


    # New Serializer for User Progress Data
class UserProgressSerializer(serializers.Serializer):
    # This serializer will define the structure of the data sent to the frontend
    # for rendering charts. It doesn't map directly to a single model.
    # We will populate its fields manually in the view.

    total_quizzes_attempted = serializers.IntegerField()
    average_score_percentage = serializers.FloatField()
    last_5_quizzes_scores = serializers.ListField(
        child=serializers.DictField(
            child=serializers.FloatField() # e.g., {'score': 80, 'total': 100}
        )
    )
    