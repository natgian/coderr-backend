from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from offers_app.api.permissions import IsBusinessUserForCreate, IsOfferCreatorOrReadOnly
from offers_app.api.serializers import OfferDetailSerializer, OfferSerializer
from offers_app.models import Offer, OfferDetail


class OfferViewSet(viewsets.ModelViewSet):
    """A viewset for managing offers, providing CRUD operations for the Offer model."""

    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated, IsBusinessUserForCreate, IsOfferCreatorOrReadOnly]

    def get_permissions(self):
        if self.action == "list":
            return [AllowAny()]
        return super().get_permissions()


class OfferDetailView(generics.RetrieveAPIView):
    """View for retrieving details of a specific offer detail."""

    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
