from django.contrib.auth import get_user_model

from rest_framework import serializers

from profiles_app.models import Profile

User = get_user_model()


class ProfileDetailSerializer(serializers.ModelSerializer):
    """Serializer for the Profile model, including related user fields."""

    username = serializers.CharField(source="user.username", read_only=True)
    type = serializers.CharField(source="user.type", read_only=True)
    email = serializers.EmailField(source="user.email")
    file = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Profile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
            "email",
            "created_at",
        ]
        read_only_fields = ["user", "created_at"]

    def validate_email(self, value):
        """Validate that the provided email address is unique across users, excluding the current user."""
        user_id = getattr(self.instance, "user_id", None)

        if User.objects.filter(email=value).exclude(pk=user_id).exists():
            raise serializers.ValidationError("This email address is already in use.")
        return value

    def update(self, instance, validated_data):
        """Update the Profile instance and the related User's email address if provided in the validated data."""
        user_data = validated_data.pop("user", {})
        email = user_data.get("email")

        if email is not None:
            instance.user.email = email
            instance.user.save(update_fields=["email"])

        return super().update(instance, validated_data)


class BusinessProfileListSerializer(serializers.ModelSerializer):
    """Serializer for the business user list view, including related user fields."""

    username = serializers.CharField(source="user.username", read_only=True)
    type = serializers.CharField(source="user.type", read_only=True)
    file = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Profile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
        ]


class CustomerProfileListSerializer(serializers.ModelSerializer):
    """Serializer for the customer user list view, including related user fields."""

    username = serializers.CharField(source="user.username", read_only=True)
    type = serializers.CharField(source="user.type", read_only=True)
    file = serializers.ImageField(required=False, allow_null=True)
    uploaded_at = serializers.DateTimeField(source="created_at", read_only=True)

    class Meta:
        model = Profile
        fields = ["user", "username", "first_name", "last_name", "file", "type", "uploaded_at"]
