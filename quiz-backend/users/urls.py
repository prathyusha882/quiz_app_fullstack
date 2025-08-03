from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    UserProfileView,
    PasswordChangeView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    EmailVerificationView,
    ResendEmailVerificationView,
    AdminUserListView,
    AdminUserDetailView,
    AdminUserStatsView,
    GoogleLoginView,
    GitHubLoginView,
    OAuthRedirectView,
)

urlpatterns = [
    # Authentication endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # User profile and settings
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('password/change/', PasswordChangeView.as_view(), name='password-change'),
    
    # Password reset
    path('password/reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    
    # Email verification
    path('email/verify/', EmailVerificationView.as_view(), name='email-verify'),
    path('email/resend-verification/', ResendEmailVerificationView.as_view(), name='resend-email-verification'),

    # Admin-only user management
    path('admin/users/', AdminUserListView.as_view(), name='admin-user-list'),
    path('admin/users/<int:id>/', AdminUserDetailView.as_view(), name='admin-user-detail'),
    path('admin/stats/', AdminUserStatsView.as_view(), name='admin-user-stats'),
    
    # OAuth endpoints
    path('google/login/', GoogleLoginView.as_view(), name='google-login'),
    path('github/login/', GitHubLoginView.as_view(), name='github-login'),
    path('oauth/<str:provider>/redirect/', OAuthRedirectView.as_view(), name='oauth-redirect'),
]
