from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import QuizAttempt, Certificate, QuizAnalytics, Leaderboard
from .services import CertificateService
from users.services import EmailService
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_quiz_completion_notification(attempt_id):
    """Send quiz completion notification asynchronously"""
    try:
        attempt = QuizAttempt.objects.get(id=attempt_id)
        success = EmailService.send_quiz_completion_email(attempt.user, attempt)
        if success:
            logger.info(f"Quiz completion notification sent to {attempt.user.email}")
        else:
            logger.error(f"Failed to send quiz completion notification to {attempt.user.email}")
        return success
    except QuizAttempt.DoesNotExist:
        logger.error(f"QuizAttempt with id {attempt_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error sending quiz completion notification: {str(e)}")
        return False

@shared_task
def generate_certificate_task(attempt_id):
    """Generate certificate asynchronously"""
    try:
        attempt = QuizAttempt.objects.get(id=attempt_id)
        certificate = CertificateService.create_certificate_for_attempt(attempt)
        
        if certificate:
            # Send certificate email
            EmailService.send_certificate_email(attempt.user, certificate)
            logger.info(f"Certificate generated for attempt {attempt_id}")
            return True
        else:
            logger.error(f"Failed to generate certificate for attempt {attempt_id}")
            return False
    except QuizAttempt.DoesNotExist:
        logger.error(f"QuizAttempt with id {attempt_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error generating certificate: {str(e)}")
        return False

@shared_task
def update_analytics():
    """Update quiz analytics asynchronously"""
    try:
        from quizzes.models import Quiz
        
        for quiz in Quiz.objects.all():
            analytics, created = QuizAnalytics.objects.get_or_create(quiz=quiz)
            analytics.update_analytics()
        
        logger.info("Analytics updated successfully")
        return True
    except Exception as e:
        logger.error(f"Error updating analytics: {str(e)}")
        return False

@shared_task
def update_leaderboard():
    """Update leaderboard asynchronously"""
    try:
        from quizzes.models import Quiz
        
        for quiz in Quiz.objects.all():
            # Clear existing leaderboard entries
            Leaderboard.objects.filter(quiz=quiz).delete()
            
            # Get all completed attempts for this quiz
            attempts = QuizAttempt.objects.filter(
                quiz=quiz,
                is_completed=True,
                is_valid=True
            ).order_by('-percentage_score', 'time_taken')
            
            # Create leaderboard entries
            for rank, attempt in enumerate(attempts, 1):
                Leaderboard.objects.create(
                    quiz=quiz,
                    user=attempt.user,
                    attempt=attempt,
                    score=attempt.score,
                    percentage_score=attempt.percentage_score,
                    time_taken=attempt.time_taken,
                    rank=rank
                )
        
        logger.info("Leaderboard updated successfully")
        return True
    except Exception as e:
        logger.error(f"Error updating leaderboard: {str(e)}")
        return False

@shared_task
def cleanup_expired_sessions():
    """Clean up expired quiz sessions"""
    try:
        from quizzes.models import QuizSession
        
        # Find sessions older than 24 hours
        expired_sessions = QuizSession.objects.filter(
            started_at__lt=timezone.now() - timedelta(hours=24),
            is_active=True
        )
        
        expired_count = expired_sessions.count()
        expired_sessions.update(is_active=False)
        
        logger.info(f"Cleaned up {expired_count} expired sessions")
        return expired_count
    except Exception as e:
        logger.error(f"Error cleaning up expired sessions: {str(e)}")
        return 0

@shared_task
def process_quiz_completion(attempt_id):
    """Process quiz completion - update analytics, leaderboard, and send notifications"""
    try:
        attempt = QuizAttempt.objects.get(id=attempt_id)
        
        # Update analytics
        update_analytics.delay()
        
        # Update leaderboard
        update_leaderboard.delay()
        
        # Send completion notification
        send_quiz_completion_notification.delay(attempt_id)
        
        # Generate certificate if passed
        if attempt.passed:
            generate_certificate_task.delay(attempt_id)
        
        logger.info(f"Quiz completion processed for attempt {attempt_id}")
        return True
    except QuizAttempt.DoesNotExist:
        logger.error(f"QuizAttempt with id {attempt_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error processing quiz completion: {str(e)}")
        return False 