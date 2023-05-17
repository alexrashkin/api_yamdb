from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_staff)
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_staff)
        )


class IsAdminOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ('DELETE', 'PUT', 'PATCH'):
            if request.user.is_authenticated:
                return request.user.role == 'admin'
        else:
            return True

    def has_permission(self, request, view):
        if (request.method in SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.role == 'admin')):
            return True


class AuthorAdminModeratorOrReadOnly(permissions.BasePermission):
    """
    GET всех объектов - Доступно без токена.

    POST объекта - Аутентифицированные пользователи.

    GET объекта - Доступно без токена.

    PATCH объекта - Автор комментария, модератор или администратор.

    DEL объекта - Автор комментария, модератор или администратор.
    """

    def has_permission(self, request, view):
        return (request.method == 'GET'
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user
                or request.method == 'GET'
                or ((request.method == 'PATCH' or request.method == 'DELETE')
                    and (request.user.is_admin or request.user.is_moderator)
                    )
                )
