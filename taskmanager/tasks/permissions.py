from rest_framework.permissions import BasePermission

class IsAdminOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name="Admin").exists():
            return True
        return obj.owner == request.user
