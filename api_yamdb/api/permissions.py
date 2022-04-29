from rest_framework.permissions import SAFE_METHODS, BasePermission


class AdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin
