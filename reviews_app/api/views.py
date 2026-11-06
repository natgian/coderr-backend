from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from reviews_app.api.filters import ReviewFilter
from reviews_app.api.permissions import IsCustomerUserForCreate, IsReviewCreatorOrReadOnly
from reviews_app.api.serializers import ReviewSerializer
from reviews_app.models import Review


class ReviewViewSet(viewsets.ModelViewSet):
    """A viewset for managing reviews, providing CRUD operations and handling review-related requests."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = ReviewFilter

    def get_permissions(self):
        """Override the default permission classes based on the action being performed."""
        if self.action == "create":
            return [IsAuthenticated(), IsCustomerUserForCreate()]

        if self.action in ("update", "partial_update", "destroy"):
            return [IsAuthenticated(), IsReviewCreatorOrReadOnly()]

        return super().get_permissions()
