from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission, SAFE_METHODS

User = get_user_model()


class IsAdmin(BasePermission):
    """
    Разрешает доступ только администраторам или для безопасных методов.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.is_superuser
                or request.user.role == User.Role.ADMIN
            )
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.role == User.Role.ADMIN
        )


class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return (
                request.user == obj.author
                or request.user.role in {User.Role.MODERATOR, User.Role.ADMIN}
                or request.user.is_superuser
            )
        return False
