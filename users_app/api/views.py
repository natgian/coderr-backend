from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import RegistrationSerializer


class RegistrationView(CreateAPIView):
    """API endpoint for creating a new user and returning a token."""

    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        """Handle the creation of a new user and return an authentication token."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        created_user = serializer.save()
        token, created = Token.objects.get_or_create(user=created_user)
        response_data = {
            "token": token.key,
            "username": created_user.username,
            "email": created_user.email,
            "user_id": created_user.id,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
