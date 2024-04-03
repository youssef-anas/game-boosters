from rest_framework.permissions import BasePermission

class IsBooster(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_booster:
            return True
        return False
