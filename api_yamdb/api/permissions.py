from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_admin
            or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_admin
            or request.user.is_staff
        )


class AuthorAdminModeratorOrReadOnly(permissions.BasePermission):
    """
    GET всех объектов - Доступно без токена.
    POST объекта - Аутентифицированные пользователи

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
