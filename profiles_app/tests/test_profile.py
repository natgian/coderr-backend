from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status

from profiles_app.api.serializers import ProfileSerializer
from test_utils.base_setup import BaseSetupTestCase

User = get_user_model()


class ProfileDetailTests(BaseSetupTestCase):
    """Tests for retrieving profile details of a user."""

    def test_profile_detail_200_success(self):
        """Ensure that an authenticated user can retrieve profile details successfully."""
        url = self.get_profile_url(self.customer_profile)
        self.authenticate(self.customer_user)

        response = self.client.get(url)

        expected_data = ProfileSerializer(
            self.customer_profile,
            context={"request": response.wsgi_request},
        ).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.data["user"], self.customer_user.id)
        self.assertEqual(response.data["username"], self.customer_user.username)
        self.assertEqual(response.data["first_name"], self.customer_profile.first_name)
        self.assertEqual(response.data["last_name"], self.customer_profile.last_name)
        self.assertEqual(response.data["file"], response.wsgi_request.build_absolute_uri(self.customer_profile.file.url))
        self.assertEqual(response.data["location"], self.customer_profile.location)
        self.assertEqual(response.data["tel"], self.customer_profile.tel)
        self.assertEqual(response.data["description"], self.customer_profile.description)
        self.assertEqual(response.data["working_hours"], self.customer_profile.working_hours)
        self.assertEqual(response.data["type"], self.customer_user.type)
        self.assertEqual(response.data["email"], self.customer_user.email)

    def test_profile_detail_200_success_empty_profile_fields(self):
        """Ensure that an authenticated user can retrieve profile details successfully even if the profile fields are empty."""
        url = self.get_profile_url(self.empty_profile)
        self.authenticate(self.empty_pf_user)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"], self.empty_pf_user.id)
        self.assertEqual(response.data["username"], self.empty_pf_user.username)
        self.assertEqual(response.data["first_name"], "")
        self.assertEqual(response.data["last_name"], "")
        self.assertIsNone(response.data["file"])
        self.assertEqual(response.data["location"], "")
        self.assertEqual(response.data["tel"], "")
        self.assertEqual(response.data["description"], "")
        self.assertEqual(response.data["working_hours"], "")
        self.assertEqual(response.data["type"], "customer")
        self.assertEqual(response.data["email"], self.empty_pf_user.email)

    def test_profile_detail_401_fail_not_authenticated(self):
        """Ensure retrieving a profile fails with an error 401 if the user is not authenticated."""
        url = self.get_profile_url(self.customer_profile)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_detail_404_fail_not_found(self):
        """Ensure retrieving a profile fails with an error 404 if the profile does not exist."""
        url = reverse("profile-detail", kwargs={"pk": 99999})
        self.authenticate(self.customer_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
