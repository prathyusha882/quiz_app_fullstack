from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from django.utils import timezone

from .models import User
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserProfileSerializer,
    UserUpdateSerializer,
    PasswordChangeSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    EmailVerificationSerializer,
    ResendEmailVerificationSerializer,
    AdminUserSerializer,
    UserStatsSerializer
)
from .services import EmailService
from .tasks import send_verification_email_task, send_password_reset_email_task

# 🔐 Helper to generate JWT tokens
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# 🔸 Registration View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        print(f"Registration request data: {request.data}")
        
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            print(f"Registration validation errors: {serializer.errors}")
            return Response({
                "error": "Registration failed",
                "details": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            user_data = UserProfileSerializer(user).data
            
            # Send verification email asynchronously
            send_verification_email_task.delay(user.id)
            
            print(f"User registered successfully: {user.username}")
            
            return Response({
                "user": user_data,
                "message": "User registered successfully. Please check your email for verification.",
                "token": tokens['access'],
                "refresh_token": tokens['refresh']
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"Registration error: {e}")
            return Response({
                "error": "Registration failed",
                "details": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

# 🔸 Login View
class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = get_tokens_for_user(user)
            user_data = UserProfileSerializer(user).data
            
            # Update last login
            user.last_login = timezone.now()
            user.save()
            
            return Response({
                "user": user_data,
                "message": "Login successful",
                "token": tokens['access'],
                "refresh_token": tokens['refresh']
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": "Invalid credentials",
                "details": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

# 🔸 Logout View (blacklists refresh token)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"error": "Invalid token or error during logout"}, status=status.HTTP_400_BAD_REQUEST)

# 🔸 Profile View (self view/update)
class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserProfileSerializer

# 🔸 Password Change View
class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordChangeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "Password change failed", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# 🔸 Password Reset Request View
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Send password reset email asynchronously
            send_password_reset_email_task.delay(user.id)
            return Response({"message": "Password reset email sent"}, status=status.HTTP_200_OK)
        return Response({"error": "Password reset request failed", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# 🔸 Password Reset Confirm View
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
        return Response({"error": "Password reset failed", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# 🔸 Email Verification View
class EmailVerificationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = EmailVerificationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Email verified successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "Email verification failed", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# 🔸 Resend Email Verification View
class ResendEmailVerificationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ResendEmailVerificationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Verification email sent"}, status=status.HTTP_200_OK)
        return Response({"error": "Failed to send verification email", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# 🔸 Admin: List all users
class AdminUserListView(generics.ListAPIView):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUser]

# 🔸 Admin: View/Update/Delete user by ID
class AdminUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance == request.user:
            return Response({"detail": "You cannot delete your own account."}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

# 🔸 Admin: User Statistics
class AdminUserStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        verified_users = User.objects.filter(email_verified=True).count()
        students = User.objects.filter(role='student').count()
        instructors = User.objects.filter(role='instructor').count()
        admins = User.objects.filter(role='admin').count()
        
        recent_registrations = User.objects.filter(
            date_joined__gte=timezone.now() - timezone.timedelta(days=7)
        ).values('username', 'email', 'role', 'date_joined')[:10]
        
        stats = {
            'total_users': total_users,
            'active_users': active_users,
            'verified_users': verified_users,
            'students': students,
            'instructors': instructors,
            'admins': admins,
            'recent_registrations': list(recent_registrations)
        }
        
        serializer = UserStatsSerializer(stats)
        return Response(serializer.data)
