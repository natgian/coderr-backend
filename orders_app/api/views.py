from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orders_app.api.permissions import OrderPermission
from orders_app.api.serializers import OrderUpdateSerializer, OrderSerializer
from orders_app.models import Order

User = get_user_model()


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

    def get_queryset(self):
        """Return the queryset of orders based on the authenticated user's type and permissions."""
        queryset = super().get_queryset()
        user = self.request.user

        if user.is_staff:
            return queryset

        if user.type == "customer":
            return queryset.filter(customer_user=user)

        if user.type == "business":
            return queryset.filter(business_user=user)

        return queryset.none()


class OrderCountView(APIView):
    """A view for retrieving the count of in-progress orders for a specific business user."""

    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        get_object_or_404(User, pk=business_user_id, type="business")

        order_count = Order.objects.filter(business_user_id=business_user_id, status="in_progress").count()

        return Response({"order_count": order_count})
