# quiz-backend/users/serializers.py
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import User
from .services import EmailService

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'is_active']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'confirm_password']
        extra_kwargs = {
            'username': {'min_length': 3, 'max_length': 30},
            'first_name': {'max_length': 30},
            'last_name': {'max_length': 30},
        }
    
    def validate_username(self, value):
        """Validate username uniqueness and format"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        
        # Check for valid characters
        import re
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError("Username can only contain letters, numbers, and underscores.")
        
        return value
    
    def validate_email(self, value):
        """Validate email uniqueness and format"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        
        # Basic email format validation
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, value):
            raise serializers.ValidationError("Please enter a valid email address.")
        
        return value
    
    def validate_password(self, value):
        """Validate password strength"""
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value
    
    def validate(self, data):
        """Validate password confirmation"""
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
    
    def create(self, validated_data):
        """Create user with validated data"""
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            is_active=False  # Require email verification
        )
        
        # Send email verification
        EmailService.send_email_verification(user)
        
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid username or password.")
            if not user.is_active:
                raise serializers.ValidationError("Account is not active. Please verify your email.")
            data['user'] = user
        else:
            raise serializers.ValidationError("Must include username and password.")
        
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
    
    def validate_email(self, value):
        """Validate email uniqueness when updating"""
        user = self.instance
        if User.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value
    
    def validate_new_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value
    
    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("New passwords do not match.")
        return data

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

class UserStatsSerializer(serializers.Serializer):
    total_quizzes_taken = serializers.IntegerField()
    passed_quizzes = serializers.IntegerField()
    average_score = serializers.FloatField()
    total_courses_enrolled = serializers.IntegerField()
    completed_courses = serializers.IntegerField()

class AdminUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class AdminUserStatsSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    active_users = serializers.IntegerField()
    new_users_this_month = serializers.IntegerField()
    verified_users = serializers.IntegerField()
