# quiz-backend/users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login', 'email_verified_status')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'last_login', 'password')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    
    def email_verified_status(self, obj):
        """Display email verification status with colored badge"""
        if obj.is_active:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Verified</span>'
            )
        else:
            return format_html(
                '<span style="color: red; font-weight: bold;">✗ Unverified</span>'
            )
    email_verified_status.short_description = 'Email Status'
    
    def get_queryset(self, request):
        """Add custom queryset with additional filtering options"""
        qs = super().get_queryset(request)
        return qs.select_related()
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of superusers by non-superusers"""
        if obj and obj.is_superuser:
            return request.user.is_superuser
        return super().has_delete_permission(request, obj)
    
    def has_change_permission(self, request, obj=None):
        """Prevent non-superusers from modifying superuser accounts"""
        if obj and obj.is_superuser:
            return request.user.is_superuser
        return super().has_change_permission(request, obj)
    
    actions = ['activate_users', 'deactivate_users', 'send_verification_email', 'export_users']
    
    def activate_users(self, request, queryset):
        """Bulk activate users"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} users have been activated.')
    activate_users.short_description = "Activate selected users"
    
    def deactivate_users(self, request, queryset):
        """Bulk deactivate users (except superusers)"""
        # Prevent deactivating superusers
        non_superusers = queryset.filter(is_superuser=False)
        updated = non_superusers.update(is_active=False)
        self.message_user(request, f'{updated} users have been deactivated.')
    deactivate_users.short_description = "Deactivate selected users"
    
    def send_verification_email(self, request, queryset):
        """Send verification email to selected users"""
        from django.core.mail import send_mail
        from django.template.loader import render_to_string
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        from django.contrib.auth.tokens import default_token_generator
        
        count = 0
        for user in queryset:
            if not user.is_active:
                # Generate verification token
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                # Send verification email
                verification_url = f"{request.scheme}://{request.get_host()}/verify-email/{uid}/{token}/"
                
                email_context = {
                    'user': user,
                    'verification_url': verification_url,
                    'site_name': 'Quiz App'
                }
                
                html_message = render_to_string('users/email_verification.html', email_context)
                plain_message = f"Please verify your email by clicking this link: {verification_url}"
                
                try:
                    send_mail(
                        subject='Verify Your Email - Quiz App',
                        message=plain_message,
                        from_email=None,  # Use default from settings
                        recipient_list=[user.email],
                        html_message=html_message
                    )
                    count += 1
                except Exception as e:
                    self.message_user(request, f'Failed to send email to {user.email}: {str(e)}')
        
        self.message_user(request, f'Verification emails sent to {count} users.')
    send_verification_email.short_description = "Send verification email to selected users"
    
    def export_users(self, request, queryset):
        """Export user data to CSV"""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Username', 'Email', 'First Name', 'Last Name', 'Is Active', 'Is Staff', 'Date Joined', 'Last Login'])
        
        for user in queryset:
            writer.writerow([
                user.username,
                user.email,
                user.first_name,
                user.last_name,
                user.is_active,
                user.is_staff,
                user.date_joined,
                user.last_login
            ])
        
        return response
    export_users.short_description = "Export selected users to CSV"

# Custom admin site configuration
admin.site.site_header = "Quiz App Administration"
admin.site.site_title = "Quiz App Admin"
admin.site.index_title = "Welcome to Quiz App Administration"

# Add custom admin actions
def get_admin_actions():
    """Get custom admin actions for the admin site"""
    return {
        'user_management': {
            'title': 'User Management',
            'actions': [
                'activate_users',
                'deactivate_users',
                'send_verification_email',
                'export_users'
            ]
        }
    }