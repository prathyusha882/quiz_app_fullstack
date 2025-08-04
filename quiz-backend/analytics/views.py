from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.db.models import Count, Avg
from django.utils import timezone
from datetime import timedelta
from .models import UserAnalytics, SystemAnalytics, PerformanceMetrics, EventTracking, ErrorLog
from quizzes.models import Quiz
from results.models import QuizAttempt
from users.models import User
from courses.models import Course, CourseEnrollment

class UserAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Calculate user statistics
        quiz_attempts = QuizAttempt.objects.filter(user=user)
        total_quizzes = quiz_attempts.count()
        passed_quizzes = quiz_attempts.filter(passed=True).count()
        average_score = quiz_attempts.aggregate(Avg('percentage_score'))['percentage_score__avg'] or 0
        
        return Response({
            'user_id': user.id,
            'total_quizzes_taken': total_quizzes,
            'passed_quizzes': passed_quizzes,
            'average_score': round(average_score, 2),
            'last_activity': user.last_activity
        }, status=status.HTTP_200_OK)

class UserEventsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        events = EventTracking.objects.filter(user=request.user).order_by('-timestamp')[:50]
        
        event_data = []
        for event in events:
            event_data.append({
                'event_type': event.event_type,
                'event_data': event.event_data,
                'timestamp': event.timestamp,
                'ip_address': event.ip_address
            })
        
        return Response(event_data, status=status.HTTP_200_OK)

class SystemAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        # System-wide statistics
        total_users = User.objects.count()
        total_quizzes = Quiz.objects.count()
        total_attempts = QuizAttempt.objects.count()
        avg_quiz_score = QuizAttempt.objects.aggregate(Avg('percentage_score'))['percentage_score__avg'] or 0
        
        return Response({
            'total_users': total_users,
            'total_quizzes': total_quizzes,
            'total_attempts': total_attempts,
            'average_quiz_score': round(avg_quiz_score, 2)
        }, status=status.HTTP_200_OK)

class PerformanceMetricsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        # Get performance metrics
        metrics = PerformanceMetrics.objects.order_by('-timestamp')[:10]
        
        metrics_data = []
        for metric in metrics:
            metrics_data.append({
                'timestamp': metric.timestamp,
                'response_time_avg': metric.response_time_avg,
                'memory_usage': metric.memory_usage,
                'cpu_usage': metric.cpu_usage,
                'disk_usage': metric.disk_usage,
                'active_connections': metric.active_connections
            })
        
        return Response(metrics_data, status=status.HTTP_200_OK)

class ErrorLogView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        errors = ErrorLog.objects.order_by('-timestamp')[:50]
        
        error_data = []
        for error in errors:
            error_data.append({
                'error_type': error.error_type,
                'error_message': error.error_message,
                'stack_trace': error.stack_trace,
                'timestamp': error.timestamp,
                'user_id': error.user_id,
                'ip_address': error.ip_address
            })
        
        return Response(error_data, status=status.HTTP_200_OK)

class QuizAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        # Quiz analytics
        quizzes = Quiz.objects.annotate(
            attempt_count=Count('attempts'),
            avg_score=Avg('attempts__percentage_score')
        )
        
        quiz_data = []
        for quiz in quizzes:
            quiz_data.append({
                'quiz_id': quiz.id,
                'quiz_title': quiz.title,
                'attempt_count': quiz.attempt_count,
                'average_score': round(quiz.avg_score or 0, 2)
            })
        
        return Response(quiz_data, status=status.HTTP_200_OK)

class QuizDetailAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, quiz_id):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            quiz = Quiz.objects.get(id=quiz_id)
            attempts = QuizAttempt.objects.filter(quiz=quiz)
            
            # Calculate detailed analytics
            total_attempts = attempts.count()
            completed_attempts = attempts.filter(is_completed=True).count()
            avg_score = attempts.aggregate(Avg('percentage_score'))['percentage_score__avg'] or 0
            avg_time = attempts.aggregate(Avg('time_taken'))['time_taken__avg']
            
            # Score distribution
            score_ranges = {
                '0-50': attempts.filter(percentage_score__lt=50).count(),
                '50-70': attempts.filter(percentage_score__gte=50, percentage_score__lt=70).count(),
                '70-90': attempts.filter(percentage_score__gte=70, percentage_score__lt=90).count(),
                '90-100': attempts.filter(percentage_score__gte=90).count()
            }
            
            return Response({
                'quiz_id': quiz.id,
                'quiz_title': quiz.title,
                'total_attempts': total_attempts,
                'completed_attempts': completed_attempts,
                'completion_rate': round((completed_attempts / total_attempts * 100) if total_attempts > 0 else 0, 2),
                'average_score': round(avg_score, 2),
                'average_time': str(avg_time) if avg_time else 'N/A',
                'score_distribution': score_ranges
            }, status=status.HTTP_200_OK)
            
        except Quiz.DoesNotExist:
            return Response({'error': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)

class CourseAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        # Get course analytics
        courses = Course.objects.annotate(
            enrollment_count=Count('courseenrollment'),
            completion_count=Count('coursecertificate')
        )
        
        course_data = []
        for course in courses:
            course_data.append({
                'course_id': course.id,
                'course_title': course.title,
                'enrollment_count': course.enrollment_count,
                'completion_count': course.completion_count,
                'completion_rate': round((course.completion_count / course.enrollment_count * 100) if course.enrollment_count > 0 else 0, 2)
            })
        
        return Response(course_data, status=status.HTTP_200_OK)

class CourseDetailAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, course_id):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            course = Course.objects.get(id=course_id)
            enrollments = CourseEnrollment.objects.filter(course=course)
            
            # Calculate detailed analytics
            total_enrollments = enrollments.count()
            active_enrollments = enrollments.filter(completed_lessons__isnull=False).count()
            certificates_issued = CourseCertificate.objects.filter(course=course).count()
            
            # Progress distribution
            progress_ranges = {
                '0-25%': enrollments.filter(completed_lessons__count__lt=course.lessons.count() * 0.25).count(),
                '25-50%': enrollments.filter(completed_lessons__count__gte=course.lessons.count() * 0.25, 
                                           completed_lessons__count__lt=course.lessons.count() * 0.5).count(),
                '50-75%': enrollments.filter(completed_lessons__count__gte=course.lessons.count() * 0.5,
                                           completed_lessons__count__lt=course.lessons.count() * 0.75).count(),
                '75-100%': enrollments.filter(completed_lessons__count__gte=course.lessons.count() * 0.75).count()
            }
            
            return Response({
                'course_id': course.id,
                'course_title': course.title,
                'total_enrollments': total_enrollments,
                'active_enrollments': active_enrollments,
                'certificates_issued': certificates_issued,
                'completion_rate': round((certificates_issued / total_enrollments * 100) if total_enrollments > 0 else 0, 2),
                'progress_distribution': progress_ranges
            }, status=status.HTTP_200_OK)
            
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

class EventTrackingView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        event_type = request.data.get('event_type')
        event_data = request.data.get('event_data', {})
        
        if not event_type:
            return Response({'error': 'Event type is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create event tracking record
        EventTracking.objects.create(
            user=request.user,
            event_type=event_type,
            event_data=event_data,
            ip_address=request.META.get('REMOTE_ADDR', ''),
            timestamp=timezone.now()
        )
        
        return Response({'message': 'Event tracked successfully'}, status=status.HTTP_201_CREATED)

class AnalyticsReportsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        # Generate reports
        reports = {
            'user_growth': User.objects.count(),
            'quiz_performance': QuizAttempt.objects.count(),
            'average_score': round(QuizAttempt.objects.aggregate(Avg('percentage_score'))['percentage_score__avg'] or 0, 2)
        }
        
        return Response(reports, status=status.HTTP_200_OK)

class ExportAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        # Export analytics data (placeholder for CSV/Excel export)
        return Response({
            'message': 'Analytics export functionality',
            'available_exports': ['user_analytics', 'quiz_analytics', 'course_analytics', 'system_metrics']
        }, status=status.HTTP_200_OK) 