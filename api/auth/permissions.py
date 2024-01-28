from rest_framework import permissions, request, status
from utils.common import USER_ROLES

class IsGuest(permissions.BasePermission):
    code = status.HTTP_403_FORBIDDEN

    def has_permission(self, request: request.Request, view):
        return not bool(request.auth)

class IsAdmin(permissions.BasePermission):
    code = status.HTTP_403_FORBIDDEN

    def has_permission(self, request: request.Request, view):
        return bool(request.user and request.user.role == USER_ROLES.ADMIN.value)


class isAuthor(permissions.BasePermission):
    code = status.HTTP_403_FORBIDDEN

    def has_permission(self, request: request.Request, view):
        return bool(request.user and request.user.role == USER_ROLES.AUTHOR.value)

