# quiz-backend/users/permissions.py
from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow administrators to edit/create objects.
    Read-only access is allowed for anyone (authenticated or not).
    """
    def has_permission(self, request, view):
        # Allow GET, HEAD, OPTIONS requests for anyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to users with 'admin' role
        # This assumes your custom User model has a 'role' field
        return request.user and request.user.is_authenticated and request.user.role == 'admin'

class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin users to edit/create.
    Read-only access is allowed for any authenticated user.
    This is similar to IsAdminOrReadOnly, but specifically targets IsAdminUser checks.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff # Django's built-in is_staff check