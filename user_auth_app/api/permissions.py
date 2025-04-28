from rest_framework import permissions
from .exeptions import UserNotLoggedIn

class IsLoggedIn(permissions.BasePermission):
    """
    Custom permission to check if the user is logged in.
    If the user is not logged in, a UserNotLoggedIn exception is raised.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            raise UserNotLoggedIn
        return True