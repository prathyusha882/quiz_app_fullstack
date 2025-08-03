from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Course, Lesson, CourseEnrollment, CourseCertificate, CourseRating
from .serializers import CourseSerializer, LessonSerializer, CourseEnrollmentSerializer
from django.utils import timezone

class CourseListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        courses = Course.objects.filter(status='published')
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CourseDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, slug):
        course = get_object_or_404(Course, slug=slug, status='published')
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CourseCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, slug):
        course = get_object_or_404(Course, slug=slug)
        if not request.user.is_staff and course.created_by != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, slug):
        course = get_object_or_404(Course, slug=slug)
        if not request.user.is_staff and course.created_by != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        course.delete()
        return Response({'message': 'Course deleted'}, status=status.HTTP_204_NO_CONTENT)

class LessonListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, course_slug):
        course = get_object_or_404(Course, slug=course_slug)
        lessons = Lesson.objects.filter(course=course)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LessonDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, course_slug, lesson_slug):
        course = get_object_or_404(Course, slug=course_slug)
        lesson = get_object_or_404(Lesson, course=course, slug=lesson_slug)
        serializer = LessonSerializer(lesson)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LessonCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, course_slug):
        course = get_object_or_404(Course, slug=course_slug)
        if not request.user.is_staff and course.created_by != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(course=course)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LessonUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, course_slug, lesson_slug):
        course = get_object_or_404(Course, slug=course_slug)
        lesson = get_object_or_404(Lesson, course=course, slug=lesson_slug)
        
        if not request.user.is_staff and course.created_by != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = LessonSerializer(lesson, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseEnrollView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, slug):
        course = get_object_or_404(Course, slug=slug, status='published')
        
        # Check if already enrolled
        if CourseEnrollment.objects.filter(user=request.user, course=course).exists():
            return Response({'error': 'Already enrolled'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create enrollment
        enrollment = CourseEnrollment.objects.create(
            user=request.user,
            course=course,
            enrolled_at=timezone.now()
        )
        
        serializer = CourseEnrollmentSerializer(enrollment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CourseUnenrollView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, slug):
        course = get_object_or_404(Course, slug=slug)
        enrollment = get_object_or_404(CourseEnrollment, user=request.user, course=course)
        
        enrollment.delete()
        return Response({'message': 'Unenrolled successfully'}, status=status.HTTP_200_OK)

class UserCourseListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        enrollments = CourseEnrollment.objects.filter(user=request.user)
        serializer = CourseEnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CourseProgressView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, course_slug):
        course = get_object_or_404(Course, slug=course_slug)
        enrollment = get_object_or_404(CourseEnrollment, user=request.user, course=course)
        
        # Calculate progress
        total_lessons = course.lessons.count()
        completed_lessons = enrollment.completed_lessons.count()
        progress_percentage = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
        
        return Response({
            'course': course.title,
            'total_lessons': total_lessons,
            'completed_lessons': completed_lessons,
            'progress_percentage': progress_percentage,
            'enrolled_at': enrollment.enrolled_at
        }, status=status.HTTP_200_OK)

class LessonProgressView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, course_slug, lesson_slug):
        course = get_object_or_404(Course, slug=course_slug)
        lesson = get_object_or_404(Lesson, course=course, slug=lesson_slug)
        enrollment = get_object_or_404(CourseEnrollment, user=request.user, course=course)
        
        is_completed = enrollment.completed_lessons.filter(id=lesson.id).exists()
        
        return Response({
            'lesson': lesson.title,
            'is_completed': is_completed,
            'content': lesson.content
        }, status=status.HTTP_200_OK)
    
    def post(self, request, course_slug, lesson_slug):
        course = get_object_or_404(Course, slug=course_slug)
        lesson = get_object_or_404(Lesson, course=course, slug=lesson_slug)
        enrollment = get_object_or_404(CourseEnrollment, user=request.user, course=course)
        
        # Mark lesson as completed
        enrollment.completed_lessons.add(lesson)
        
        return Response({'message': 'Lesson marked as completed'}, status=status.HTTP_200_OK)

class CourseCertificateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, slug):
        course = get_object_or_404(Course, slug=slug)
        enrollment = get_object_or_404(CourseEnrollment, user=request.user, course=course)
        
        # Check if course is completed
        total_lessons = course.lessons.count()
        completed_lessons = enrollment.completed_lessons.count()
        
        if completed_lessons < total_lessons:
            return Response({'error': 'Course not completed'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate or get existing certificate
        certificate, created = CourseCertificate.objects.get_or_create(
            user=request.user,
            course=course,
            defaults={
                'issued_at': timezone.now(),
                'certificate_number': f"CERT-{course.slug.upper()}-{request.user.id}"
            }
        )
        
        return Response({
            'certificate_number': certificate.certificate_number,
            'course_title': course.title,
            'user_name': request.user.get_full_name(),
            'issued_at': certificate.issued_at,
            'download_url': f"/api/courses/{slug}/certificate/download/"
        }, status=status.HTTP_200_OK)

class CourseRatingView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, slug):
        course = get_object_or_404(Course, slug=slug)
        rating_value = request.data.get('rating')
        review = request.data.get('review', '')
        
        if not rating_value or not (1 <= rating_value <= 5):
            return Response({'error': 'Invalid rating'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create or update rating
        rating, created = CourseRating.objects.get_or_create(
            user=request.user,
            course=course,
            defaults={'rating': rating_value, 'review': review}
        )
        
        if not created:
            rating.rating = rating_value
            rating.review = review
            rating.save()
        
        return Response({'message': 'Rating submitted'}, status=status.HTTP_200_OK)

class CourseReviewsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, slug):
        course = get_object_or_404(Course, slug=slug)
        ratings = CourseRating.objects.filter(course=course)
        
        reviews = []
        for rating in ratings:
            reviews.append({
                'user_name': rating.user.get_full_name(),
                'rating': rating.rating,
                'review': rating.review,
                'created_at': rating.created_at
            })
        
        return Response(reviews, status=status.HTTP_200_OK) 