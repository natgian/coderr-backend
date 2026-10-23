from rest_framework import permissions


class OrderPermission(permissions.BasePermission):
    """Permission class for managing order actions based on user type and action being performed."""

    def has_permission(self, request, view):
        """
        Determine if the user has permission to perform the requested action.

        - Only customers can create orders
        - Only business users can update orders
        - Only staff users can delete orders
        """
        if view.action == "create":
            return request.user.type == "customer"

        if view.action in ["update", "partial_update"]:
            return request.user.type == "business"

        if view.action == "destroy":
            return request.user.is_staff

        return True
