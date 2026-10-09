from django.db.models import Min

from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from offers_app.api.permissions import IsBusinessUserForCreate, IsOfferCreatorOrReadOnly
from offers_app.api.serializers import OfferDetailSerializer, OfferListSerializer, OfferSerializer
from offers_app.models import Offer, OfferDetail


class OfferViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing offers, including listing, creating, retrieving, updating, and deleting offers. It uses different serializers and permissions based on the action being performed.
    """

    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [
        IsAuthenticated,
        IsBusinessUserForCreate,
        IsOfferCreatorOrReadOnly,
    ]

    def get_queryset(self):
        """
        Override the default queryset to annotate the minimum price of offer details for the 'list' action. For other actions, return the default queryset.
        """
        queryset = super().get_queryset()

        if self.action == "list":
            queryset = queryset.select_related("user__profile").prefetch_related("details")
            queryset = queryset.annotate(
                min_price=Min("details__price"),
                min_delivery_time=Min("details__delivery_time_in_days"),
            )
        elif self.action == "retrieve":
            queryset = queryset.prefetch_related("details")

        return queryset

    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the action being performed. For the 'list' action, use OfferListSerializer, otherwise OfferSerializer.
        """
        if self.action == "list":
            return OfferListSerializer
        return OfferSerializer

    def get_permissions(self):
        """
        Override the default permission classes based on the action being performed. For the 'list' action, allow any user to access the view. For other actions, use the default permissions defined in the class.
        """
        if self.action == "list":
            return [AllowAny()]
        return super().get_permissions()


class OfferDetailView(generics.RetrieveAPIView):
    """View for retrieving details of a specific offer detail."""

    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
