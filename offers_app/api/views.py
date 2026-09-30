from rest_framework import viewsets

from offers_app.api.serializers import OfferSerializer
from offers_app.models import Offer


class OfferViewSet(viewsets.ModelViewSet):
    """A viewset for managing offers, providing CRUD operations for the Offer model."""

    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
