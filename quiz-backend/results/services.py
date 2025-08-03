# quiz-backend/results/services.py
from django.conf import settings
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from .models import Certificate, QuizAttempt
import io
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import logging
from django.utils import timezone
import uuid

logger = logging.getLogger(__name__)

class CertificateService:
    """Service for generating certificates"""
    
    @staticmethod
    def generate_certificate_pdf(certificate):
        """Generate PDF certificate"""
        try:
            # Create certificate directory if it doesn't exist
            cert_dir = os.path.join(settings.MEDIA_ROOT, 'certificates')
            os.makedirs(cert_dir, exist_ok=True)
            
            # Generate filename
            filename = f"certificate_{certificate.certificate_id}.pdf"
            filepath = os.path.join(cert_dir, filename)
            
            # Create PDF
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            story = []
            
            # Get styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                alignment=TA_CENTER,
                textColor=colors.darkblue
            )
            
            subtitle_style = ParagraphStyle(
                'CustomSubtitle',
                parent=styles['Heading2'],
                fontSize=16,
                spaceAfter=20,
                alignment=TA_CENTER,
                textColor=colors.grey
            )
            
            body_style = ParagraphStyle(
                'CustomBody',
                parent=styles['Normal'],
                fontSize=12,
                spaceAfter=12,
                alignment=TA_LEFT
            )
            
            # Add content
            story.append(Paragraph("CERTIFICATE OF COMPLETION", title_style))
            story.append(Spacer(1, 20))
            
            # Certificate details
            story.append(Paragraph(f"This is to certify that", body_style))
            story.append(Paragraph(f"<b>{certificate.attempt.user.get_full_name() or certificate.attempt.user.username}</b>", title_style))
            story.append(Paragraph("has successfully completed the quiz", body_style))
            story.append(Paragraph(f"<b>{certificate.attempt.quiz.title}</b>", subtitle_style))
            story.append(Spacer(1, 20))
            
            # Performance details
            performance_data = [
                ['Quiz Title:', certificate.attempt.quiz.title],
                ['Score:', f"{certificate.attempt.percentage_score}%"],
                ['Correct Answers:', f"{certificate.attempt.correct_answers}/{certificate.attempt.total_questions}"],
                ['Time Taken:', str(certificate.attempt.time_taken).split('.')[0] if certificate.attempt.time_taken else 'N/A'],
                ['Completion Date:', certificate.attempt.submitted_at.strftime('%B %d, %Y')],
                ['Certificate ID:', certificate.certificate_number],
            ]
            
            performance_table = Table(performance_data, colWidths=[2*inch, 4*inch])
            performance_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ]))
            
            story.append(performance_table)
            story.append(Spacer(1, 30))
            
            # Signature section
            story.append(Paragraph("This certificate is issued on", body_style))
            story.append(Paragraph(f"<b>{timezone.now().strftime('%B %d, %Y')}</b>", body_style))
            story.append(Spacer(1, 40))
            
            # Add signature line
            signature_data = [
                ['_________________', '_________________'],
                ['Quiz Administrator', 'Date'],
            ]
            
            signature_table = Table(signature_data, colWidths=[3*inch, 3*inch])
            signature_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            
            story.append(signature_table)
            
            # Build PDF
            doc.build(story)
            
            # Save file path to certificate
            certificate.pdf_file = f'certificates/{filename}'
            certificate.save()
            
            return True
            
        except Exception as e:
            print(f"Error generating certificate PDF: {str(e)}")
            return False
    
    @staticmethod
    def create_certificate_for_attempt(attempt):
        """Create a certificate for a completed quiz attempt"""
        try:
            # Check if certificate already exists
            if hasattr(attempt, 'certificate'):
                return attempt.certificate
            
            # Create certificate
            certificate = Certificate.objects.create(
                attempt=attempt,
                certificate_id=uuid.uuid4(),
                certificate_data={
                    'user_name': attempt.user.get_full_name() or attempt.user.username,
                    'quiz_title': attempt.quiz.title,
                    'score': attempt.percentage_score,
                    'completion_date': attempt.submitted_at.isoformat(),
                }
            )
            
            # Generate PDF
            CertificateService.generate_certificate_pdf(certificate)
            
            return certificate
            
        except Exception as e:
            print(f"Error creating certificate: {str(e)}")
            return None
    
    @staticmethod
    def generate_leaderboard(quiz):
        """Generate leaderboard for a quiz"""
        from .models import Leaderboard
        
        # Get all completed attempts for this quiz
        attempts = quiz.attempts.filter(is_completed=True, is_valid=True).order_by(
            '-percentage_score', 'time_taken'
        )
        
        # Clear existing leaderboard entries
        Leaderboard.objects.filter(quiz=quiz).delete()
        
        # Create new leaderboard entries
        for rank, attempt in enumerate(attempts, 1):
            Leaderboard.objects.create(
                quiz=quiz,
                user=attempt.user,
                attempt=attempt,
                score=attempt.score,
                percentage_score=attempt.percentage_score,
                time_taken=attempt.time_taken or attempt.time_taken,
                rank=rank
            )
        
        logger.info(f"Leaderboard generated for quiz {quiz.id}")
        return attempts.count()
    
    @staticmethod
    def update_quiz_analytics(quiz):
        """Update analytics for a quiz"""
        from .models import QuizAnalytics
        
        analytics, created = QuizAnalytics.objects.get_or_create(quiz=quiz)
        analytics.update_analytics()
        
        logger.info(f"Analytics updated for quiz {quiz.id}")
        return analytics 