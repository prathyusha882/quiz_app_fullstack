from rest_framework import serializers
from .models import Course, Lesson, CourseEnrollment, CourseCertificate, CourseRating

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ('course', 'created_at', 'updated_at')

class CourseEnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    
    class Meta:
        model = CourseEnrollment
        fields = '__all__'
        read_only_fields = ('user', 'enrolled_at')

class CourseCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCertificate
        fields = '__all__'
        read_only_fields = ('user', 'course', 'issued_at', 'certificate_number')

class CourseRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRating
        fields = '__all__'
        read_only_fields = ('user', 'course', 'created_at') 