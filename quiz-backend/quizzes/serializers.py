# quiz-backend/quizzes/serializers.py
from rest_framework import serializers
from .models import Quiz, Question, Option

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'is_correct']
        read_only_fields = ['id'] # ID is read-only when creating/updating via API

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, required=False) # Nested serializer for options

    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'options']
        read_only_fields = ['id']

    def create(self, validated_data):
        options_data = validated_data.pop('options', [])
        question = Question.objects.create(**validated_data)
        for option_data in options_data:
            Option.objects.create(question=question, **option_data)
        return question

    def update(self, instance, validated_data):
        options_data = validated_data.pop('options', None)

        instance.text = validated_data.get('text', instance.text)
        instance.question_type = validated_data.get('question_type', instance.question_type)
        instance.save()

        if options_data is not None:
            # Handle options: update existing, create new, delete missing
            existing_options = {option.id: option for option in instance.options.all()}
            for option_data in options_data:
                option_id = option_data.get('id')
                if option_id and option_id in existing_options:
                    # Update existing option
                    option = existing_options.pop(option_id)
                    for attr, value in option_data.items():
                        setattr(option, attr, value)
                    option.save()
                else:
                    # Create new option
                    Option.objects.create(question=instance, **option_data)

            # Delete options that were in existing_options but not in new options_data
            for option_to_delete in existing_options.values():
                option_to_delete.delete()

        return instance


class QuizSerializer(serializers.ModelSerializer):
    question_count = serializers.ReadOnlyField() # From the @property in Quiz model

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'slug', 'description', 'difficulty', 'duration', 'is_active', 'created_at', 'updated_at', 'question_count']
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at', 'question_count']

# Serializer for getting questions for taking a quiz (without correct answers)
class TakeQuizQuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()  # Use method field to get shuffled options

    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'options']
        # Correct answers are intentionally excluded here for the user-facing quiz.

    def get_options(self, obj):
        # Use shuffled options if available, otherwise use regular options
        if hasattr(obj, '_shuffled_options'):
            return OptionSerializer(obj._shuffled_options, many=True).data
        else:
            return OptionSerializer(obj.options.all(), many=True).data

# Serializer for admin to get questions with correct answers
class AdminQuestionDetailSerializer(QuestionSerializer):
    # Inherits from QuestionSerializer, which already includes `is_correct` in OptionSerializer
    pass