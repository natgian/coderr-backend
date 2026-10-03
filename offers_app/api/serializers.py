from rest_framework import serializers

from offers_app.models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the OfferDetail model, used for nested serialization within the OfferSerializer.
    """

    class Meta:
        model = OfferDetail
        fields = ["id", "title", "revisions", "delivery_time_in_days", "price", "features", "offer_type"]
        read_only_fields = ["offer"]


class OfferSerializer(serializers.ModelSerializer):
    """
    Serializer for the Offer model, including nested serialization for OfferDetail instances.
    """

    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ["id", "title", "image", "description", "details"]

    def validate_details(self, value):
        """Validate that exactly three OfferDetail instances are provided in the 'details' field."""
        if self.instance is None and len(value) != 3:
            raise serializers.ValidationError("Exactly 3 details are required.")
        return value

    def create(self, validate_data):
        """Create an Offer instance along with its nested OfferDetail instances."""

        details_data = validate_data.pop("details")
        current_user = self.context["request"].user

        offer = Offer.objects.create(user=current_user, **validate_data)

        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)

        return offer

    def update(self, instance, validated_data):
        """Update an Offer instance along with its nested OfferDetail instances."""
        details_data = validated_data.pop("details", [])

        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()

        for detail_data in details_data:
            target_offer_type = detail_data["offer_type"]
            detail_in_db = instance.details.get(offer_type=target_offer_type)

            for field, value in detail_data.items():
                if field == "offer_type":
                    continue
                setattr(detail_in_db, field, value)

            detail_in_db.save()

        return instance
