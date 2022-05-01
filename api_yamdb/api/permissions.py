from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, BasePermission

User = get_user_model()


class AdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.role == User.ADMIN


class AuthorAdminModeratorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (
            obj.author == request.user or (
                request.user.is_superuser
            ) or (
                request.user.is_admin
            ) or (
                request.user.is_moderator
            )
        )


class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
            return False
        return False


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == User.ADMIN:
                return True
            return False
        return False


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == User.MODERATOR:
                return True
            return False
        return False


class IsUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == User.USER:
                return True
            return False
        return False
