from rest_framework import permissions


class AuthorAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_authenticated
            and request.user.is_admin
        )