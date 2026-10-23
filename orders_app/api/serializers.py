from rest_framework import serializers
from rest_framework.exceptions import NotFound

from offers_app.models import OfferDetail
from orders_app.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for the Order model, handling serialization and deserialization of order instances."""

    price = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False, read_only=True)

    offer_detail_id = serializers.IntegerField(write_only=True, min_value=1, source="offer_detail")

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

    def validate_offer_detail_id(self, value):
        """Validate that the provided offer_detail_id corresponds to an existing OfferDetail instance."""
        try:
            return OfferDetail.objects.get(pk=value)
        except OfferDetail.DoesNotExist:
            raise NotFound(detail="Offer detail not found.")

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


class OrderUpdateSerializer(OrderSerializer):
    """
    Serializer for updating an Order instance, excluding the offer_detail_id field from the update process and allowing the status field to be updated.
    """

    offer_detail_id = None

    class Meta(OrderSerializer.Meta):
        fields = []
        for field in OrderSerializer.Meta.fields:
            if field != "offer_detail_id":
                fields.append(field)

        read_only_fields = []
        for field in fields:
            if field != "status":
                read_only_fields.append(field)

    def validate(self, attrs):
        """
        Validate that the request only contains the status field for updating an order instance.
        Raise a ValidationError if any other fields are present in the request data."""
        request_data = self.initial_data

        for field in request_data.keys():
            if field != "status":
                raise serializers.ValidationError("Invalid fields in the request.")
        return attrs
