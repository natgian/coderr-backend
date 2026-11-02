from rest_framework import permissions


class IsCustomerUserForCreate(permissions.BasePermission):
    """Permission class to allow only users of type "customer" to create reviews."""

    def has_permission(self, request, view):
        """
        Determine if the user has permission to perform the requested action.

        Only users from type "customer" can create reviews.
        """
        if view.action == "create":
            return request.user.type == "customer"

        return True


class IsReviewCreatorOrReadOnly(permissions.BasePermission):
    """
    Permission class to allow only the creator of a review to update or delete it, while allowing read-only access to others.
    """

    def has_object_permission(self, request, view, obj):
        """
        Allow all users to read reviews, but restrict updating and deleting to the creator of the review.
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.reviewer == request.user
