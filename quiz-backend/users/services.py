# quiz-backend/users/services.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
import logging

logger = logging.getLogger(__name__)

class EmailService:
    """Service for sending emails"""
    
    @staticmethod
    def send_email(to_email, subject, html_content, text_content=None):
        """Send email using configured email backend"""
        try:
            if not text_content:
                text_content = strip_tags(html_content)
            
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[to_email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    @staticmethod
    def send_email_verification(user):
        """Send email verification link"""
        token = user.generate_email_verification_token()
        verification_url = f"{settings.FRONTEND_URL}/verify-email/{token}"
        
        subject = "Verify Your Email - Quiz App"
        html_content = render_to_string('users/email_verification.html', {
            'user': user,
            'verification_url': verification_url,
            'site_name': settings.SITE_NAME
        })
        
        return EmailService.send_email(user.email, subject, html_content)
    
    @staticmethod
    def send_password_reset(user):
        """Send password reset link"""
        token = user.generate_password_reset_token()
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{token}"
        
        subject = "Reset Your Password - Quiz App"
        html_content = render_to_string('users/password_reset.html', {
            'user': user,
            'reset_url': reset_url,
            'site_name': settings.SITE_NAME
        })
        
        return EmailService.send_email(user.email, subject, html_content)
    
    @staticmethod
    def send_quiz_completion_email(user, quiz_attempt):
        """Send quiz completion notification"""
        subject = f"Quiz Completed - {quiz_attempt.quiz.title}"
        html_content = render_to_string('users/quiz_completion.html', {
            'user': user,
            'attempt': quiz_attempt,
            'site_name': settings.SITE_NAME
        })
        
        return EmailService.send_email(user.email, subject, html_content)
    
    @staticmethod
    def send_certificate_email(user, certificate):
        """Send certificate email"""
        subject = f"Your Certificate - {certificate.attempt.quiz.title}"
        html_content = render_to_string('users/certificate_email.html', {
            'user': user,
            'certificate': certificate,
            'site_name': settings.SITE_NAME
        })
        
        return EmailService.send_email(user.email, subject, html_content)
    
    @staticmethod
    def send_welcome_email(user):
        """Send welcome email to new users"""
        try:
            subject = "Welcome to Quiz App!"
            html_message = render_to_string('users/welcome_email.html', {
                'user': user,
                'dashboard_url': f"{settings.FRONTEND_URL}/dashboard"
            })
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            logger.info(f"Welcome email sent to {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send welcome email: {str(e)}")
            return False 