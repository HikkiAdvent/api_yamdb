from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

User = get_user_model()


class AdminPermission(BasePermission):
    """Разрешение для доступа только для администраторов."""
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            return request.user.role == User.Role.ADMIN
        return False
