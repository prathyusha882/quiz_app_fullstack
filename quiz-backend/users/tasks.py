from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import User
from .services import EmailService
from results.models import QuizAttempt, Certificate
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_verification_email_task(user_id):
    """Send email verification asynchronously"""
    try:
        user = User.objects.get(id=user_id)
        success = EmailService.send_verification_email(user)
        if success:
            logger.info(f"Verification email sent successfully to {user.email}")
        else:
            logger.error(f"Failed to send verification email to {user.email}")
        return success
    except User.DoesNotExist:
        logger.error(f"User with id {user_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error sending verification email: {str(e)}")
        return False

@shared_task
def send_password_reset_email_task(user_id):
    """Send password reset email asynchronously"""
    try:
        user = User.objects.get(id=user_id)
        success = EmailService.send_password_reset_email(user)
        if success:
            logger.info(f"Password reset email sent successfully to {user.email}")
        else:
            logger.error(f"Failed to send password reset email to {user.email}")
        return success
    except User.DoesNotExist:
        logger.error(f"User with id {user_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error sending password reset email: {str(e)}")
        return False

@shared_task
def send_quiz_completion_email_task(attempt_id):
    """Send quiz completion notification asynchronously"""
    try:
        attempt = QuizAttempt.objects.get(id=attempt_id)
        success = EmailService.send_quiz_completion_email(attempt.user, attempt)
        if success:
            logger.info(f"Quiz completion email sent to {attempt.user.email}")
        else:
            logger.error(f"Failed to send quiz completion email to {attempt.user.email}")
        return success
    except QuizAttempt.DoesNotExist:
        logger.error(f"QuizAttempt with id {attempt_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error sending quiz completion email: {str(e)}")
        return False

@shared_task
def send_certificate_email_task(certificate_id):
    """Send certificate email asynchronously"""
    try:
        certificate = Certificate.objects.get(id=certificate_id)
        success = EmailService.send_certificate_email(certificate.attempt.user, certificate)
        if success:
            logger.info(f"Certificate email sent to {certificate.attempt.user.email}")
        else:
            logger.error(f"Failed to send certificate email to {certificate.attempt.user.email}")
        return success
    except Certificate.DoesNotExist:
        logger.error(f"Certificate with id {certificate_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error sending certificate email: {str(e)}")
        return False

@shared_task
def send_reminder_emails():
    """Send reminder emails to users who haven't completed quizzes"""
    try:
        # Find users who registered but haven't taken any quizzes
        users_without_attempts = User.objects.filter(
            role='student',
            email_verified=True,
            is_active=True,
            quiz_attempts__isnull=True
        ).distinct()
        
        # Find users who started quizzes but didn't complete them
        incomplete_attempts = QuizAttempt.objects.filter(
            is_completed=False,
            started_at__lt=timezone.now() - timedelta(days=1)
        )
        
        reminder_count = 0
        
        # Send reminders to users without attempts
        for user in users_without_attempts[:50]:  # Limit to 50 emails per run
            try:
                # This would need a proper reminder email template
                logger.info(f"Sending reminder to {user.email}")
                reminder_count += 1
            except Exception as e:
                logger.error(f"Error sending reminder to {user.email}: {str(e)}")
        
        # Send reminders for incomplete attempts
        for attempt in incomplete_attempts[:50]:  # Limit to 50 emails per run
            try:
                logger.info(f"Sending completion reminder to {attempt.user.email}")
                reminder_count += 1
            except Exception as e:
                logger.error(f"Error sending completion reminder: {str(e)}")
        
        logger.info(f"Sent {reminder_count} reminder emails")
        return reminder_count
        
    except Exception as e:
        logger.error(f"Error in send_reminder_emails: {str(e)}")
        return 0

@shared_task
def cleanup_expired_tokens():
    """Clean up expired email verification and password reset tokens"""
    try:
        # Clean up expired email verification tokens (older than 24 hours)
        expired_verification = User.objects.filter(
            email_verification_sent_at__lt=timezone.now() - timedelta(hours=24),
            email_verified=False
        )
        expired_verification.update(email_verification_token=None, email_verification_sent_at=None)
        
        # Clean up expired password reset tokens (older than 1 hour)
        expired_reset = User.objects.filter(
            password_reset_sent_at__lt=timezone.now() - timedelta(hours=1),
            password_reset_token__isnull=False
        )
        expired_reset.update(password_reset_token=None, password_reset_sent_at=None)
        
        logger.info("Cleaned up expired tokens")
        return True
    except Exception as e:
        logger.error(f"Error cleaning up expired tokens: {str(e)}")
        return False 