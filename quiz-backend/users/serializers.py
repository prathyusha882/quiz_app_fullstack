# quiz-backend/users/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User
from .services import EmailService

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm', 'role']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True}
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        
        # Send email verification
        EmailService.send_email_verification(user)
        
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include username and password')
        
        return attrs

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 
                 'profile_picture', 'bio', 'date_of_birth', 'phone_number', 
                 'email_verified', 'account_created_at', 'last_activity']
        read_only_fields = ['id', 'username', 'email_verified', 'account_created_at', 'last_activity']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'profile_picture', 'bio', 
                 'date_of_birth', 'phone_number']
    
    def update(self, instance, validated_data):
        # Handle profile picture upload
        if 'profile_picture' in validated_data:
            # Delete old profile picture if it exists
            if instance.profile_picture:
                instance.profile_picture.delete(save=False)
        
        return super().update(instance, validated_data)

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled")
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email address")
        return value
    
    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        EmailService.send_password_reset(user)
        return user

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])
    new_password_confirm = serializers.CharField()
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def validate_token(self, value):
        try:
            user = User.objects.get(password_reset_token=value)
            if not user.password_reset_sent_at:
                raise serializers.ValidationError("Invalid reset token")
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid reset token")
        return value
    
    def save(self):
        token = self.validated_data['token']
        new_password = self.validated_data['new_password']
        
        user = User.objects.get(password_reset_token=token)
        user.set_password(new_password)
        user.clear_password_reset_token()
        user.save()
        
        return user

class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField()
    
    def validate_token(self, value):
        try:
            user = User.objects.get(email_verification_token=value)
            if user.email_verified:
                raise serializers.ValidationError("Email already verified")
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid verification token")
        return value
    
    def save(self):
        token = self.validated_data['token']
        user = User.objects.get(email_verification_token=token)
        user.verify_email_token(token)
        return user

class ResendEmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
            if user.email_verified:
                raise serializers.ValidationError("Email already verified")
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email address")
        return value
    
    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        EmailService.send_email_verification(user)
        return user

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role',
                 'is_active', 'email_verified', 'account_created_at', 'last_activity']
        read_only_fields = ['id', 'account_created_at', 'last_activity']

class UserStatsSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    active_users = serializers.IntegerField()
    verified_users = serializers.IntegerField()
    students = serializers.IntegerField()
    instructors = serializers.IntegerField()
    admins = serializers.IntegerField()
    recent_registrations = serializers.ListField()
