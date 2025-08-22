from rest_framework import permissions, request, status
from utils.common import USER_ROLES

class IsAdmin(permissions.IsAuthenticated):
    code = status.HTTP_403_FORBIDDEN

    def has_permission(self, request: request.Request, view):
        return (
            super().has_permission(request, view)
            and request.user.role == USER_ROLES.ADMIN.value
        )


class IsAuthor(permissions.IsAuthenticated):
    code = status.HTTP_403_FORBIDDEN

    def has_permission(self, request: request.Request, view):
        return (
            super().has_permission(request, view)
            and request.user.role == USER_ROLES.AUTHOR.value
        )
