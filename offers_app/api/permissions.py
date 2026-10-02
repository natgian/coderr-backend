from rest_framework import permissions


class IsBusinessUserForCreate(permissions.BasePermission):
    """Permission for creating offers: only business users can create offers."""

    def has_permission(self, request, view):
        """Allow all users to read offers, but restrict creation to business users."""
        if view.action != "create":
            return True
        return request.user.type == "business"


class IsOfferCreatorOrReadOnly(permissions.BasePermission):
    """Permission for offer detail actions: only the creator can modify, others can read."""

    def has_object_permission(self, request, view, obj):
        """Allow all users to read offers, but restrict modifications to the creator of the offer."""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user
