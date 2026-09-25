from rest_framework import serializers

from profiles_app.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
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
