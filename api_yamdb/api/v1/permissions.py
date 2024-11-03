from rest_framework import permissions


class IsAdminOrModerator(permissions.BasePermission):
    """Разрешение для администратора и модератора."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (getattr(request.user, 'is_admin', False)
                 or getattr(request.user, 'is_moderator', False))
        )


class AnonimReadOnly(permissions.BasePermission):
    """Разрешает анонимному пользователю только безопасные запросы."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAdminModeratorOrAuthor(permissions.BasePermission):
    """
    Разрешение для админа, модератора или автора редактирования объектов,
    иначе - только безопасные запросы.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (getattr(request.user, 'is_admin', False)
                 or getattr(request.user, 'is_moderator', False)
                 or obj.author == request.user)
        )


class ReviewCommentPermissions(permissions.BasePermission):
    """
    Разрешения для создания, обновления и удаления отзывов и комментариев.
    """

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated
            and (
                request.user == obj.author
                or getattr(request.user, 'is_moderator', False)
                or getattr(request.user, 'is_admin', False)
            )
        )
