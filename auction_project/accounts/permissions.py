from rest_framework.permissions import BasePermission, IsAuthenticated, \
                                       SAFE_METHODS

from .models import Profile


class IsNotAuthenticated(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return True
        return request.user.is_superuser or request.user.is_staff


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        # import pdb; pdb.set_trace()
        is_owner = request.user.username == obj.user.username
        if is_owner or request.user.is_staff or request.user.is_superuser:
            return True
        return False
