from rest_framework.permissions import SAFE_METHODS, BasePermission


class AdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff or request.user.is_superuser


class OpenAuctionsOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        import ipdb; ipdb.set_trace()
        if request.user.is_staff or request.user.is_superuser:
            sadasdas
            return True
        sadasdas
        return obj.status == 'Open'
