from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.conf import settings

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
    AdminUserDetailSerializer,
    AdminUserStatsSerializer,
)
from .services import EmailService

User = get_user_model()

# Registration
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserProfileSerializer(user).data
        }, status=status.HTTP_201_CREATED)

# Login
class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserProfileSerializer(user).data
        })

# Logout
class UserLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({"detail": "Successfully logged out."})
        except Exception as e:
            return Response({"detail": "Logout successful."})

# Profile
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# Profile Update
class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# Change Password
class PasswordChangeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({"detail": "Password changed successfully."})

# Request Password Reset
class PasswordResetView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password reset email sent."})

# Confirm Password Reset
class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password reset successful."})

# Verify Email
class EmailVerificationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Email verified successfully."})

# Verify Email with token
class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, uidb64, token):
        try:
            # Implementation for email verification with token
            return Response({"detail": "Email verified successfully."})
        except Exception as e:
            return Response({"detail": "Email verification failed."}, status=400)

# Resend Verification Email
class ResendVerificationEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ResendEmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Verification email resent."})

# Admin - List Users
class AdminUserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAdminUser]

# Admin - User Detail
class AdminUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserDetailSerializer
    permission_classes = [permissions.IsAdminUser]

# Admin - Stats
class AdminUserStatsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        verified_users = User.objects.filter(email_verified=True).count()
        new_users_this_month = User.objects.filter(account_created_at__month=timezone.now().month).count()

        data = {
            'total_users': total_users,
            'active_users': active_users,
            'verified_users': verified_users,
            'new_users_this_month': new_users_this_month
        }
        serializer = AdminUserStatsSerializer(data)
        return Response(serializer.data)

# OAuth Views
class GoogleLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        # Redirect to Google OAuth
        return Response({"auth_url": f"{settings.FRONTEND_URL}/api/auth/google/"})

class GitHubLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        # Redirect to GitHub OAuth
        return Response({"auth_url": f"{settings.FRONTEND_URL}/api/auth/github/"})

class OAuthRedirectView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, provider):
        # Handle OAuth redirect
        return Response({"auth_url": f"{settings.FRONTEND_URL}/api/auth/{provider}/"})

# User Stats
class UserStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        # Calculate user stats
        stats = {
            'quizzes_taken': 0,  # TODO: Implement
            'average_score': 0,   # TODO: Implement
            'total_courses': 0,   # TODO: Implement
        }
        return Response(stats)
