from rest_framework import serializers
from .models import ProctoringSession, Violation, ProctoringSettings

class ProctoringSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProctoringSession
        fields = '__all__'
        read_only_fields = ('user', 'started_at', 'ip_address', 'user_agent')

class ViolationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Violation
        fields = '__all__'
        read_only_fields = ('user', 'session', 'timestamp')

class ProctoringSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProctoringSettings
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at') 