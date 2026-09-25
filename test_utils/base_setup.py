from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from profiles_app.models import Profile

User = get_user_model()


class BaseSetupTestCase(APITestCase):
    def setUp(self):
        """Set up initial data for test cases, including users, tokens, and profiles."""

        # USERS
        # Create customer user
        self.customer_user = User.objects.create_user(
            username="customerUser",
            email="customer@mail.com",
            password="customerPassword",
            type="customer",
        )

        # Create business user
        self.business_user = User.objects.create_user(
            username="businessUser",
            email="business@mail.com",
            password="businessPassword",
            type="business",
        )

        # Create empty profile user
        self.empty_pf_user = User.objects.create_user(
            username="emptyProfileUser",
            email="emptyProfle@mail.com",
            password="emptyProfilePassword",
            type="customer",
        )

        # PROFILES
        # Create customer user profile
        self.customer_profile = Profile.objects.create(
            user=self.customer_user,
            first_name="Max",
            last_name="Muster",
            file="profile_picture.jpg",
            location="Zürich",
            tel="123456789",
            description="This is a description.",
            working_hours="8.00 - 17.00",
        )

        # Create empty user profile
        self.empty_profile = Profile.objects.create(
            user=self.empty_pf_user,
            first_name="",
            last_name="",
            file=None,
            location="",
            tel="",
            description="",
            working_hours="",
        )

    def authenticate(self, user):
        token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def get_profile_url(self, profile):
        return reverse("profile-detail", kwargs={"pk": profile.pk})
