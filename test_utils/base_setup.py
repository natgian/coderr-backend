from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from offers_app.models import Offer, OfferDetail
from profiles_app.models import Profile

User = get_user_model()


class BaseSetupTestCase(APITestCase):
    def setUp(self):
        """Set up initial data for test cases, including users, tokens, profiles, offers and offer details."""

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
        self.business_user2 = User.objects.create_user(
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
        self.business_profile2 = Profile.objects.create(
            user=self.business_user2,
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
        # Create offers
        self.offer_web = Offer.objects.create(
            user=self.business_user,
            title="Webdesign & Entwicklung-Paket",
            description="Erstellung einer modernen, responsiven Website für Ihren digitalen Auftritt.",
        )
        self.detail_web_basic = OfferDetail.objects.create(
            offer=self.offer_web,
            title="Basic Web",
            revisions=2,
            delivery_time_in_days=10,
            price=450,
            features=["One-Page Website", "Responsives Design", "Kontaktformular"],
            offer_type="basic",
        )
        self.detail_web_standard = OfferDetail.objects.create(
            offer=self.offer_web,
            title="Standard Web",
            revisions=4,
            delivery_time_in_days=20,
            price=950,
            features=["Website mit bis zu 5 Unterseiten", "Responsives Design", "Kontaktformular", "Basis-SEO-Optimierung", "CMS-Einrichtung (WordPress)"],
            offer_type="standard",
        )
        self.detail_web_premium = OfferDetail.objects.create(
            offer=self.offer_web,
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

        self.offer_graphic = Offer.objects.create(
            user=self.business_user,
            title="Grafikdesign-Paket",
            description="Ein umfassendes Grafikdesign-Paket für Unternehmen.",
        )
        self.detail_graphic_basic = OfferDetail.objects.create(
            offer=self.offer_graphic,
            title="Basic Design",
            revisions=2,
            delivery_time_in_days=5,
            price=100,
            features=["Logo Design", "Visitenkarte"],
            offer_type="basic",
        )
        self.detail_graphic_standard = OfferDetail.objects.create(
            offer=self.offer_graphic,
            title="Standard Design",
            revisions=5,
            delivery_time_in_days=7,
            price=200,
            features=["Logo Design", "Visitenkarte", "Briefpapier"],
            offer_type="standard",
        )
        self.detail_graphic_premium = OfferDetail.objects.create(
            offer=self.offer_graphic,
            title="Premium Design",
            revisions=10,
            delivery_time_in_days=10,
            price=500,
            features=["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"],
            offer_type="premium",
        )

        self.offer_social = Offer.objects.create(
            user=self.business_user2,
            title="Social Media Marketing-Paket",
            description="Professionelle Betreuung und Content-Erstellung für Ihre Social-Media-Kanäle.",
        )
        self.detail_social_basic = OfferDetail.objects.create(
            offer=self.offer_social,
            title="Basic Social",
            revisions=1,
            delivery_time_in_days=7,
            price=150,
            features=["3 Post-Vorlagen", "Kanal-Optimierung"],
            offer_type="basic",
        )
        self.detail_social_standard = OfferDetail.objects.create(
            offer=self.offer_social,
            title="Standard Social",
            revisions=3,
            delivery_time_in_days=10,
            price=350,
            features=["6 Post-Vorlagen", "Kanal-Optimierung", "1 Video/Reel", "Hashtag-Analyse"],
            offer_type="standard",
        )
        self.detail_social_premium = OfferDetail.objects.create(
            offer=self.offer_social,
            title="Premium Social",
            revisions=5,
            delivery_time_in_days=14,
            price=750,
            features=["12 Post-Vorlagen", "Kanal-Optimierung", "3 Videos/Reels", "Hashtag-Analyse", "Redaktionsplan", "Monatliches Reporting"],
            offer_type="premium",
        )

    def authenticate(self, user):
        """Create a token for the given user and set the authorization header for the test client."""
        token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def get_profile_url(self, profile):
        """Return the URL for the profile detail view for the given profile."""
        return reverse("profile-detail", kwargs={"pk": profile.pk})
