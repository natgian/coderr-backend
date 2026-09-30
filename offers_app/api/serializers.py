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

    def create(self, validate_data):
        """Create an Offer instance along with its nested OfferDetail instances."""

        details_data = validate_data.pop("details")
        current_user = self.context["request"].user

        offer = Offer.objects.create(user=current_user, **validate_data)

        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)

        return offer
