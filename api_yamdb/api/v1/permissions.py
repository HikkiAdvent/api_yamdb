from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import Role


class IsAdmin(BasePermission):
    """
    Разрешает доступ только администраторам.
    """
    def has_permission(self, request, view):
        return getattr(request.user, 'role', None) == Role.ADMIN.value


class IsModerator(BasePermission):
    """
    Разрешает доступ только модераторам.
    """
    def has_permission(self, request, view):
        return getattr(request.user, 'role', None) == Role.MODERATOR.value


class IsAuthor(BasePermission):
    """
    Разрешает доступ автору объекта или для безопасных методов.
    """
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user


class IsAnonymousUser(BasePermission):
    """
    Разрешает доступ только анонимным пользователям и только к безопасным методам.
    """
    def has_permission(self, request, view):
        return request.user.is_anonymous and request.method in SAFE_METHODS


class IsAdminOrModeratorOrAuthorOrReadOnly(BasePermission):
    """
    Комплексная проверка для анонимов, админов, модераторов и авторов.
    """
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or IsAdmin().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return (
            IsAdmin().has_permission(request, view) or
            IsModerator().has_permission(request, view) or
            IsAuthor().has_object_permission(request, view, obj)
        )
