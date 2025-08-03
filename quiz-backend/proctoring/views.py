from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import ProctoringSession, Violation, ProctoringSettings
from .serializers import ProctoringSessionSerializer, ViolationSerializer

class StartProctoringSessionView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        quiz_id = request.data.get('quiz_id')
        if not quiz_id:
            return Response({'error': 'Quiz ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if session already exists
        existing_session = ProctoringSession.objects.filter(
            user=request.user,
            quiz_id=quiz_id,
            ended_at__isnull=True
        ).first()
        
        if existing_session:
            return Response({'error': 'Session already active'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create new proctoring session
        session = ProctoringSession.objects.create(
            user=request.user,
            quiz_id=quiz_id,
            started_at=timezone.now(),
            ip_address=request.META.get('REMOTE_ADDR', ''),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            screen_resolution=request.data.get('screen_resolution', ''),
            browser_info=request.data.get('browser_info', '')
        )
        
        serializer = ProctoringSessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProctoringSessionView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, session_id):
        session = get_object_or_404(ProctoringSession, id=session_id, user=request.user)
        serializer = ProctoringSessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EndProctoringSessionView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, session_id):
        session = get_object_or_404(ProctoringSession, id=session_id, user=request.user)
        
        if session.ended_at:
            return Response({'error': 'Session already ended'}, status=status.HTTP_400_BAD_REQUEST)
        
        session.ended_at = timezone.now()
        session.save()
        
        return Response({'message': 'Session ended successfully'}, status=status.HTTP_200_OK)

class ViolationListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if request.user.is_staff:
            violations = Violation.objects.all().order_by('-timestamp')
        else:
            violations = Violation.objects.filter(user=request.user).order_by('-timestamp')
        
        serializer = ViolationSerializer(violations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ViolationDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, violation_id):
        if request.user.is_staff:
            violation = get_object_or_404(Violation, id=violation_id)
        else:
            violation = get_object_or_404(Violation, id=violation_id, user=request.user)
        
        serializer = ViolationSerializer(violation)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ResolveViolationView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, violation_id):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        violation = get_object_or_404(Violation, id=violation_id)
        resolution_notes = request.data.get('resolution_notes', '')
        
        violation.resolved = True
        violation.resolved_by = request.user
        violation.resolved_at = timezone.now()
        violation.resolution_notes = resolution_notes
        violation.save()
        
        return Response({'message': 'Violation resolved'}, status=status.HTTP_200_OK)

class ProctoringSettingsListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        settings = ProctoringSettings.objects.all()
        return Response([{
            'id': s.id,
            'name': s.name,
            'webcam_required': s.webcam_required,
            'screen_recording': s.screen_recording,
            'browser_lock': s.browser_lock,
            'tab_switch_detection': s.tab_switch_detection,
            'fullscreen_required': s.fullscreen_required
        } for s in settings], status=status.HTTP_200_OK)

class ProctoringSettingsCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        name = request.data.get('name')
        webcam_required = request.data.get('webcam_required', False)
        screen_recording = request.data.get('screen_recording', False)
        browser_lock = request.data.get('browser_lock', False)
        tab_switch_detection = request.data.get('tab_switch_detection', False)
        fullscreen_required = request.data.get('fullscreen_required', False)
        
        settings = ProctoringSettings.objects.create(
            name=name,
            webcam_required=webcam_required,
            screen_recording=screen_recording,
            browser_lock=browser_lock,
            tab_switch_detection=tab_switch_detection,
            fullscreen_required=fullscreen_required,
            created_by=request.user
        )
        
        return Response({
            'id': settings.id,
            'name': settings.name,
            'webcam_required': settings.webcam_required,
            'screen_recording': settings.screen_recording,
            'browser_lock': settings.browser_lock,
            'tab_switch_detection': settings.tab_switch_detection,
            'fullscreen_required': settings.fullscreen_required
        }, status=status.HTTP_201_CREATED)

class ProctoringSettingsDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, settings_id):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        settings = get_object_or_404(ProctoringSettings, id=settings_id)
        serializer = ProctoringSettingsSerializer(settings)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProctoringSettingsUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, settings_id):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        settings = get_object_or_404(ProctoringSettings, id=settings_id)
        serializer = ProctoringSettingsSerializer(settings, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProctoringReportsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        # Generate proctoring reports
        total_sessions = ProctoringSession.objects.count()
        active_sessions = ProctoringSession.objects.filter(ended_at__isnull=True).count()
        total_violations = Violation.objects.count()
        unresolved_violations = Violation.objects.filter(resolved=False).count()
        
        return Response({
            'total_sessions': total_sessions,
            'active_sessions': active_sessions,
            'total_violations': total_violations,
            'unresolved_violations': unresolved_violations
        }, status=status.HTTP_200_OK)

class ProctoringReportDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, session_id):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        session = get_object_or_404(ProctoringSession, id=session_id)
        violations = Violation.objects.filter(session=session)
        
        return Response({
            'session_id': session.id,
            'user': session.user.get_full_name(),
            'quiz_id': session.quiz_id,
            'started_at': session.started_at,
            'ended_at': session.ended_at,
            'duration': str(session.ended_at - session.started_at) if session.ended_at else 'Active',
            'violations_count': violations.count(),
            'violations': [{
                'type': v.violation_type,
                'description': v.description,
                'timestamp': v.timestamp,
                'resolved': v.resolved
            } for v in violations]
        }, status=status.HTTP_200_OK) 