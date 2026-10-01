from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from offers_app.models import Offer, OfferDetail
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

        # Create business user
        self.second_business_user = User.objects.create_user(
            username="businessUser2",
            email="business2@mail.com",
            password="business2Password",
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

        # Create business user profile
        self.business_profile = Profile.objects.create(
            user=self.business_user,
            first_name="John",
            last_name="Carter",
            file="profile_picture.jpg",
            location="New York",
            tel="987654321",
            description="This is a description.",
            working_hours="9.00 - 18.00",
        )

        # Create business user profile
        self.second_business_profile = Profile.objects.create(
            user=self.second_business_user,
            first_name="Jane",
            last_name="Butler",
            file="profile_picture.jpg",
            location="San Francisco",
            tel="111154321",
            description="This is a description.",
            working_hours="6.00 - 16.00",
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

        # OFFERS & DETAILS
        # Create offer
        self.offer_one = Offer.objects.create(
            user=self.business_user,
            title="Webdesign & Entwicklung-Paket",
            image=None,
            description="Erstellung einer modernen, responsiven Website für Ihren digitalen Auftritt.",
        )

        OfferDetail.objects.create(
            offer=self.offer_one,
            title="Basic Web",
            revisions=2,
            delivery_time_in_days=10,
            price=450,
            features=["One-Page Website", "Responsives Design", "Kontaktformular"],
            offer_type="basic",
        )

        OfferDetail.objects.create(
            offer=self.offer_one,
            title="Standard Web",
            revisions=4,
            delivery_time_in_days=20,
            price=950,
            features=["Website mit bis zu 5 Unterseiten", "Responsives Design", "Kontaktformular", "Basis-SEO-Optimierung", "CMS-Einrichtung (WordPress)"],
            offer_type="standard",
        )

        OfferDetail.objects.create(
            offer=self.offer_one,
            title="Premium Web",
            revisions=8,
            delivery_time_in_days=30,
            price=2200,
            features=[
                "Website mit unbegrenzten Unterseiten",
                "Responsives Design",
                "Kontaktformular",
                "Erweiterte SEO-Optimierung",
                "CMS-Einrichtung (WordPress)",
                "Onlineshop-Integration",
                "1 Monat technischer Support",
            ],
            offer_type="premium",
        )

    def authenticate(self, user):
        token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def get_profile_url(self, profile):
        return reverse("profile-detail", kwargs={"pk": profile.pk})
