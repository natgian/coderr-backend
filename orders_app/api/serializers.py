from rest_framework import serializers

from offers_app.models import OfferDetail
from orders_app.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for the Order model, handling serialization and deserialization of order instances."""

    price = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False, read_only=True)

    offer_detail_id = serializers.PrimaryKeyRelatedField(source="offer_detail", queryset=OfferDetail.objects.all(), write_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "offer_detail_id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        """Create an order instance based on the provided offer_detail and the authenticated customer user."""
        offer_detail = validated_data["offer_detail"]
        customer = self.context["request"].user

        return Order.objects.create(
            offer_detail=offer_detail,
            customer_user=customer,
            business_user=offer_detail.offer.user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
        )
