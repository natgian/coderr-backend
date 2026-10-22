from rest_framework import permissions


class IsCustomerUserForCreate(permissions.BasePermission):
    """Permission for creating orders: only customer users can create orders."""

    def has_permission(self, request, view):
        """Allow all users to read orders, but restrict creation to customer users."""
        if view.action != "create":
            return True
        return request.user.type == "customer"
