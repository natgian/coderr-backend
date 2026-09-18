from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

User = get_user_model()


class AuthTests(APITestCase):
    """Test cases for user registration and authentication."""

    def test_user_registration_201_success(self):
        """Ensure a user can register successfully with valid data and receives a token."""
        url = reverse("registration")
        data = {
            "username": "exampleUser",
            "email": "example@mail.com",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username=data["username"]).exists())

        created_user = User.objects.get(username="exampleUser")
        token = Token.objects.get(user=created_user)
        expected_data = {
            "token": token.key,
            "username": created_user.username,
            "email": created_user.email,
            "user_id": created_user.id,
        }

        self.assertEqual(created_user.type, "customer")
        self.assertEqual(response.data, expected_data)
