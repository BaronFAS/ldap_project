from rest_framework import permissions


class IsCompanyAdminOrSuperuser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated and hasattr(request.user, 'company'):
            if request.user.company == obj.company:
                return True
        elif not request.user.is_authenticated:
            return False
        return False
