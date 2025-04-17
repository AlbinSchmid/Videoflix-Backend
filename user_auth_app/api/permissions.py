from rest_framework import permissions
from .exeptions import UserNotLoggedIn

class IsLoggedIn(permissions.BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            raise UserNotLoggedIn
        return True