from rest_framework.permissions import BasePermission

class IsBooster(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_booster
    

class IsNotBooster(BasePermission):
    """
    Custom permission to deny access to users who are boosters.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated :
            return False
        return not request.user.is_booster


