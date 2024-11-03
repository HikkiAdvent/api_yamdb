from rest_framework.permissions import BasePermission

from users.models import Role


class AdminPermission(BasePermission):
    """
    Разрешение для доступа только для администраторов.
    """

    def has_permission(self, request, view):
        return request.user.role == Role.ADMIN.value
