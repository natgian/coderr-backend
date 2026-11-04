from rest_framework import serializers

from reviews_app.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for the Review model."""

    class Meta:
        model = Review
        fields = ["id", "business_user", "reviewer", "rating", "description", "created_at", "updated_at"]
        read_only_fields = ["id", "reviewer", "created_at", "updated_at"]

    def validate(self, attrs):
        """Validate that a reviewer can only leave one review per business user."""
        reviewer = self.context["request"].user
        business_user = attrs.get("business_user") or (self.instance and self.instance.business_user)

        queryset = Review.objects.filter(reviewer=reviewer, business_user=business_user)

        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)

        if queryset.exists():
            raise serializers.ValidationError({"business_user": "You already left a review for this service provider."})

        attrs["reviewer"] = reviewer

        return attrs

    def validate_business_user(self, value):
        """Validate that the business user is of type "business" and cannot be changed once set."""
        if self.instance and value.pk != self.instance.business_user_id:
            raise serializers.ValidationError("The business user can't be changed.")

        if value.type != "business":
            raise serializers.ValidationError("The user must be a business user.")
        return value
