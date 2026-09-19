from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import CustomUser

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "repeated_password", "type"]
        extra_kwargs = {
            "password": {"write_only": True},
            "username": {"validators": []},
            "email": {"validators": []},
        }

    def validate(self, data):
        """Check that the two password fields match and check for existing users."""
        if data["password"] != data["repeated_password"]:
            raise serializers.ValidationError("Passwords do not match.")

        if (
            User.objects.filter(email=data["email"]).exists()
            or User.objects.filter(username=data["username"]).exists()
        ):
            raise serializers.ValidationError(
                {"non_field_errors": ["Username oder email address already taken"]}
            )
        return data

    def create(self, validated_data):
        """Create and return a new user."""
        validated_data.pop("repeated_password")
        user = User.objects.create_user(**validated_data)
        return user
