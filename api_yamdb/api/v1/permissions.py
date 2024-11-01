from rest_framework import permissions


class IsSuperUserOrIsAdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_superuser
                 or request.user.is_staff
                 or request.user.is_admin)
        )


class AnonimReadOnly(permissions.BasePermission):
    """Разрешает анонимному пользователю только безопасные запросы."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsSuperUserIsAdminIsModeratorIsAuthor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.is_superuser
                 or request.user.is_staff
                 or request.user.is_admin
                 or request.user.is_moderator
                 or request.user == obj.author)
        )


class ReviewCommentPermissions(permissions.BasePermission):
    """
    Разрешения для создания, обновления и удаления отзывов и комментариев.
    """
    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update', 'destroy']:
            return (
                request.user.is_authenticated
                and (
                    request.user == obj.author
                    or getattr(request.user, 'is_moderator', False)
                    or request.user.is_staff
                    or request.user.is_superuser
                )
            )
        return True
