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
        """Ensure a user can register successfully and receives a token."""
        url = reverse("registration")
        data = {
            "username": "exampleUser",
            "email": "example@mail.com",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer",
        }

        response = self.client.post(url, data, format="json")

        created_user = User.objects.get(username="exampleUser")
        token = Token.objects.get(user=created_user)
        expected_data = {
            "token": token.key,
            "username": created_user.username,
            "email": created_user.email,
            "user_id": created_user.id,
        }

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username=data["username"]).exists())
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

    def test_user_login_200_success(self):
        """Ensure a user can log in successfully and receives a token."""
        url = reverse("login")
        data = {"username": "SetupUser", "password": "setupPassword"}

        response = self.client.post(url, data, format="json")

        token = Token.objects.get(user=self.setup_user)
        expected_data = {
            "token": token.key,
            "username": self.setup_user.username,
            "email": self.setup_user.email,
            "user_id": self.setup_user.id,
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_user_login_400_fail_invalid_password_or_username(self):
        """Ensure login fails with a 400 error if the password or username is incorrect."""
        url = reverse("login")
        data_wrong_pw = {"username": "SetupUser", "password": "WRONG_Password"}

        response_wrong_pw = self.client.post(url, data_wrong_pw, format="json")

        self.assertEqual(response_wrong_pw.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid username or password", str(response_wrong_pw.data))

        data_wrong_username = {"username": "WrongUser", "password": "setupPassword"}

        response_wrong_username = self.client.post(url, data_wrong_username, format="json")

        self.assertEqual(response_wrong_username.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid username or password", str(response_wrong_username.data))

    def test_user_login_400_fail_missing_field(self):
        """Ensure login fails with a 400 error if a field is missing."""
        url = reverse("login")
        data_missing_pw = {"username": "setupUser"}

        response_missing_pw = self.client.post(url, data_missing_pw, format="json")

        self.assertEqual(response_missing_pw.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("field is required", str(response_missing_pw.data))

        data_missing_username = {"password": "setupPassword"}

        response_missing_username = self.client.post(url, data_missing_username, format="json")

        self.assertEqual(response_missing_username.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("field is required", str(response_missing_username.data))

    def test_user_login_400_fail_blank_fields(self):
        """Ensure lgoin fails with a 400 error if fields are blank."""
        url = reverse("login")
        data = {"username": "", "password": ""}

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("may not be blank", str(response.data))
