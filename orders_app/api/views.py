from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from orders_app.api.permissions import OrderPermission
from orders_app.api.serializers import OrderUpdateSerializer, OrderSerializer
from orders_app.models import Order


class OrderViewSet(viewsets.ModelViewSet):
    """A viewset for managing orders, providing CRUD operations and handling order-related requests."""

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, OrderPermission]

    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the action being performed.
        """
        if self.action == "partial_update":
            return OrderUpdateSerializer
        return OrderSerializer
