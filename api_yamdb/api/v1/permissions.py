from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, BasePermission

User = get_user_model()


class OnlyAdmin(BasePermission):
    """Разрешение для доступа только для администраторов."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdmin(BasePermission):
    """
    Разрешает доступ только администраторам или для безопасных методов.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin or request.method in SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and request.user.is_admin or request.method in SAFE_METHODS
        )


class IsAuthor(BasePermission):
    """
    Разрешает доступ к редактированию только авторам, модераторам,
    администратором или используется для безопасных методов.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            user.is_authenticated
            and user.is_moderator_or_admin
            or user == obj.author or request.method in SAFE_METHODS
        )
