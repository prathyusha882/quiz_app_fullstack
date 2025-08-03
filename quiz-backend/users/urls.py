from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Authentication endpoints
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/update/', views.UserUpdateView.as_view(), name='update-profile'),
    path('change-password/', views.PasswordChangeView.as_view(), name='change-password'),
    
    # Email verification and password reset
    path('verify-email/', views.EmailVerificationView.as_view(), name='verify-email'),
    path('verify-email/<str:uidb64>/<str:token>/', views.VerifyEmailView.as_view(), name='verify-email-confirm'),
    path('reset-password/', views.PasswordResetView.as_view(), name='reset-password'),
    path('reset-password/<str:uidb64>/<str:token>/', views.PasswordResetConfirmView.as_view(), name='reset-password-confirm'),
    
    # User statistics
    path('stats/', views.UserStatsView.as_view(), name='user-stats'),
    
    # Admin endpoints
    path('admin/users/', views.AdminUserListView.as_view(), name='admin-user-list'),
    path('admin/users/<int:id>/', views.AdminUserDetailView.as_view(), name='admin-user-detail'),
    path('admin/stats/', views.AdminUserStatsView.as_view(), name='admin-user-stats'),
    
    # OAuth endpoints
    path('google/login/', views.GoogleLoginView.as_view(), name='google-login'),
    path('github/login/', views.GitHubLoginView.as_view(), name='github-login'),
    path('oauth/<str:provider>/redirect/', views.OAuthRedirectView.as_view(), name='oauth-redirect'),
]
