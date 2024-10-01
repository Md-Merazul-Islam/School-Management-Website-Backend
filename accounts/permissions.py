from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsStaffOrReadOnly(BasePermission):
    """
    Custom permission to only allow staff users to edit objects.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed to staff users.
        return request.user.is_staff
