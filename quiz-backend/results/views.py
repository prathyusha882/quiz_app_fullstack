from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch, Avg
from django.db.models.functions import Cast
from django.db.models import FloatField

from quizzes.models import Quiz, Question, Option
from .models import QuizAttempt, UserAnswer
from .serializers import QuizSubmissionSerializer, QuizAttemptSerializer, UserProgressSerializer
from quizzes.serializers import TakeQuizQuestionSerializer, AdminQuestionDetailSerializer
from quizzes.serializers import OptionSerializer


class QuizSubmitView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, quiz_id, *args, **kwargs):
        user = request.user
        quiz = get_object_or_404(Quiz, pk=quiz_id, is_active=True)
        submitted_answers_data = request.data.get('answers', [])
        time_taken = request.data.get('timeTaken', '00:00')

        print(f"Received data: {request.data}")
        print(f"Answers: {submitted_answers_data}")

        if not isinstance(submitted_answers_data, list):
            return Response({"error": "Answers must be a list of objects."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            attempt = QuizAttempt.objects.create(
                user=user,
                quiz=quiz,
                total_questions=quiz.questions.count(),
                time_taken=time_taken
            )

            score = 0
            questions_for_quiz = {q.id: q for q in quiz.questions.all().prefetch_related('options')}

            for submitted_answer_entry in submitted_answers_data:
                print(f"Processing answer: {submitted_answer_entry}")
                
                # Handle both 'question_id' and 'submitted_answer' format
                question_id = submitted_answer_entry.get('question_id')
                user_submitted_answer = submitted_answer_entry.get('submitted_answer') or submitted_answer_entry.get('selected_answer')
                
                if not question_id or user_submitted_answer is None:
                    print(f"Skipping invalid answer: {submitted_answer_entry}")
                    continue

                question = questions_for_quiz.get(int(question_id))
                if not question:
                    print(f"Question not found: {question_id}")
                    continue

                is_correct = False
                chosen_option_obj = None
                chosen_text = None

                if question.question_type == 'multiple-choice':
                    chosen_option_obj = question.options.filter(text=user_submitted_answer).first()
                    if chosen_option_obj and chosen_option_obj.is_correct:
                        is_correct = True
                elif question.question_type == 'checkbox':
                    user_selected_options_texts = set(user_submitted_answer)
                    correct_options = set(opt.text for opt in question.options.filter(is_correct=True))
                    if user_selected_options_texts == correct_options and len(correct_options) > 0:
                        is_correct = True
                elif question.question_type == 'text-input':
                    user_text = str(user_submitted_answer).strip().lower()
                    correct_texts = [str(opt.text).strip().lower() for opt in question.options.filter(is_correct=True)]
                    if user_text in correct_texts and user_text != '':
                        is_correct = True
                    chosen_text = user_submitted_answer

                if is_correct:
                    score += 1

                UserAnswer.objects.create(
                    attempt=attempt,
                    question=question,
                    chosen_option=chosen_option_obj,
                    chosen_text_answer=chosen_text,
                    is_correct_answer=is_correct
                )

            attempt.score = score
            attempt.passed = (score / attempt.total_questions) * 100 >= 70
            attempt.save()

            serializer = QuizAttemptSerializer(attempt)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserResultsListView(generics.ListAPIView):
    serializer_class = QuizAttemptSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return QuizAttempt.objects.filter(user=self.request.user).order_by('-submitted_at').select_related('quiz')


class QuizAttemptDetailView(generics.RetrieveAPIView):
    serializer_class = QuizAttemptSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'

    def get_queryset(self):
        return QuizAttempt.objects.filter(user=self.request.user).select_related('quiz').prefetch_related(
            Prefetch('user_answers', queryset=UserAnswer.objects.select_related('question', 'chosen_option'))
        )


class QuizAttemptReviewView(generics.RetrieveAPIView):
    serializer_class = QuizAttemptSerializer
    permission_classes = (IsAuthenticated,)
    queryset = QuizAttempt.objects.all()
    lookup_field = 'attempt_id'

    def get_queryset(self):
        return QuizAttempt.objects.filter(user=self.request.user).select_related('quiz').prefetch_related(
            Prefetch('user_answers', queryset=UserAnswer.objects.select_related('question', 'chosen_option')),
            Prefetch('quiz__questions', queryset=Question.objects.prefetch_related('options'))
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        review_data = serializer.data
        review_questions = []

        all_quiz_questions = {q.id: q for q in instance.quiz.questions.all().prefetch_related('options')}
        user_answers_map = {ans.question_id: ans for ans in instance.user_answers.all()}

        for q_id, question_obj in all_quiz_questions.items():
            user_ans = user_answers_map.get(q_id)

            correct_answers_list = []
            if question_obj.question_type in ['multiple-choice', 'checkbox', 'text-input']:
                correct_answers_list = [opt.text for opt in question_obj.options.filter(is_correct=True)]

            review_questions.append({
                'id': question_obj.id,
                'text': question_obj.text,
                'question_type': question_obj.question_type,
                'options': OptionSerializer(question_obj.options.all(), many=True).data,
                'user_chosen_option_text': user_ans.chosen_option.text if user_ans and user_ans.chosen_option else None,
                'user_chosen_text_answer': user_ans.chosen_text_answer if user_ans else None,
                'is_user_answer_correct': user_ans.is_correct_answer if user_ans else False,
                'correct_answers': correct_answers_list,
            })

        review_data['questions_for_review'] = review_questions
        return Response(review_data)


class AdminResultsListView(generics.ListAPIView):
    queryset = QuizAttempt.objects.all().order_by('-submitted_at').select_related('user', 'quiz')
    serializer_class = QuizAttemptSerializer
    permission_classes = (IsAdminUser,)


class UserProgressView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        all_attempts = QuizAttempt.objects.filter(user=user).order_by('-submitted_at')

        total_quizzes_attempted = all_attempts.count()

        average_score_percentage = 0.0
        if total_quizzes_attempted > 0:
            try:
                avg_score_raw = all_attempts.aggregate(
                    avg_percentage=Avg(
                        (Cast('score', FloatField()) / Cast('total_questions', FloatField())) * 100
                    )
                )['avg_percentage']
                average_score_percentage = round(avg_score_raw, 2) if avg_score_raw is not None else 0.0
            except Exception as e:
                print(f"Error calculating average score: {e}")
                average_score_percentage = 0.0

        last_5_quizzes_scores = []
        for attempt in all_attempts[:5]:
            try:
                percentage = round((attempt.score / attempt.total_questions) * 100, 2) if attempt.total_questions > 0 else 0.0
                last_5_quizzes_scores.append({
                    'quiz_title': str(attempt.quiz.title),
                    'score': str(attempt.score),
                    'total': str(attempt.total_questions),
                    'percentage': str(percentage)
                })
            except Exception as e:
                print(f"Error processing attempt {attempt.id}: {e}")
                continue

        progress_data = {
            'total_quizzes_attempted': total_quizzes_attempted,
            'average_score_percentage': average_score_percentage,
            'last_5_quizzes_scores': last_5_quizzes_scores,
        }

        serializer = UserProgressSerializer(progress_data)
        return Response(serializer.data, status=status.HTTP_200_OK)
