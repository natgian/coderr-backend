from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

User = get_user_model()


class AuthTests(APITestCase):
    """Test cases for user registration and authentication."""

    def setUp(self):
        """Set up user data before each test method runs."""
        self.setup_user = User.objects.create_user(
            username="SetupUser",
            email="setup-user@mail.com",
            password="setupPassword",
            type="customer",
        )

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

    def test_user_registration_400_fail_passwords_missmatch(self):
        """Ensure registration fails with a 400 error if passwords don't match."""
        url = reverse("registration")
        data = {
            "username": "exampleUser",
            "email": "example@mail.com",
            "password": "examplePassword",
            "repeated_password": "examplePasswordddd",
            "type": "customer",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("Response Data:", response.data)

    def test_user_registration_400_fail_passwords_missing_fields(self):
        """Ensure registration fails with a 400 error if fields are missing."""
        url = reverse("registration")
        data = {
            "username": "exampleUser",
            "email": "example@mail.com",
            "password": "examplePassword",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_400_fail_existing_user(self):
        """Ensure registration fails with a 400 error if email or username already exists."""
        url = reverse("registration")
        data = {
            "username": "NewUser",
            "email": "setup-user@mail.com",
            "password": "newPassword",
            "repeated_password": "newPassword",
            "type": "customer",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
