from rest_framework import viewsets
from rest_framework.response import Response

from orders_app.api.serializers import OrderSerializer
from orders_app.models import Order


class OrderViewSet(viewsets.ModelViewSet):
    """A viewset for managing orders, providing CRUD operations and handling order-related requests."""

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
