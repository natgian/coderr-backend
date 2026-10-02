from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status

from offers_app.api.serializers import OfferSerializer
from offers_app.models import Offer, OfferDetail

from test_utils.base_setup import BaseSetupTestCase

User = get_user_model()


class OfferCreateTests(BaseSetupTestCase):
    """Tests for creating offers with nested offer details."""

    def test_create_offer_201_success(self):
        """Ensure creating an offer with three details succeeds with a 201 and returns the correct data."""
        url = reverse("offer-list")
        self.authenticate(self.business_user)
        initial_offer_count = Offer.objects.count()
        initial_detail_count = OfferDetail.objects.count()
        offer_data = {
            "title": "Grafikdesign-Paket",
            "image": None,
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {"title": "Basic Design", "revisions": 2, "delivery_time_in_days": 5, "price": 100, "features": ["Logo Design", "Visitenkarte"], "offer_type": "basic"},
                {"title": "Standard Design", "revisions": 5, "delivery_time_in_days": 7, "price": 200, "features": ["Logo Design", "Visitenkarte", "Briefpapier"], "offer_type": "standard"},
                {"title": "Premium Design", "revisions": 10, "delivery_time_in_days": 10, "price": 500, "features": ["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"], "offer_type": "premium"},
            ],
        }

        response = self.client.post(url, offer_data, format="json")

        created_offer = Offer.objects.get(id=response.data["id"])
        expected_data = OfferSerializer(created_offer, context={"request": response.wsgi_request}).data

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_data)
        self.assertEqual(created_offer.user, self.business_user)
        self.assertEqual(created_offer.details.count(), 3)
        self.assertEqual(Offer.objects.count(), initial_offer_count + 1)
        self.assertEqual(OfferDetail.objects.count(), initial_detail_count + 3)
        self.assertEqual(created_offer.title, offer_data["title"])
        self.assertEqual(created_offer.description, offer_data["description"])
        self.assertFalse(created_offer.image)

        for expected_detail in offer_data["details"]:
            db_detail = created_offer.details.filter(offer_type=expected_detail["offer_type"]).first()

            self.assertIsNotNone(db_detail, f"OfferDetail for '{expected_detail['offer_type']}' is missing in the DB.")
            self.assertEqual(db_detail.title, expected_detail["title"])
            self.assertEqual(db_detail.revisions, expected_detail["revisions"])
            self.assertEqual(db_detail.delivery_time_in_days, expected_detail["delivery_time_in_days"])
            self.assertEqual(float(db_detail.price), float(expected_detail["price"]))
            self.assertEqual(db_detail.features, expected_detail["features"])

    def test_create_offer_400_fail_fewer_than_three_details(self):
        """Ensure creating an offer fails with an error 400 if there are fewer than three details."""

        url = reverse("offer-list")
        self.authenticate(self.business_user)
        offer_data = {
            "title": "Grafikdesign-Paket",
            "image": None,
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {"title": "Basic Design", "revisions": 2, "delivery_time_in_days": 5, "price": 100, "features": ["Logo Design", "Visitenkarte"], "offer_type": "basic"},
            ],
        }

        response = self.client.post(url, offer_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_offer_400_fail_invalid_data(self):
        """Ensure creating an offer fails with an error 400 if the data is invalid."""

        url = reverse("offer-list")
        self.authenticate(self.business_user)
        offer_data = {
            "title": "",
            "image": 123,
            "details": [
                {"title": "Basic Design", "revisions": 2, "delivery_time_in_days": 5, "price": 100, "features": ["Logo Design", "Visitenkarte"], "offer_type": "basic"},
                {"title": "Standard Design", "revisions": 5, "delivery_time_in_days": 7, "price": 200, "features": ["Logo Design", "Visitenkarte", "Briefpapier"], "offer_type": "standard"},
                {"title": "Premium Design", "revisions": 10, "delivery_time_in_days": 10, "price": 500, "features": ["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"], "offer_type": "premium"},
            ],
        }

        response = self.client.post(url, offer_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_offer_401_fail_not_authenticated(self):
        """Ensure creating an offer fails with an error 401 if the user is not authenticated."""

        url = reverse("offer-list")
        offer_data = {
            "title": "Grafikdesign-Paket",
            "image": None,
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {"title": "Basic Design", "revisions": 2, "delivery_time_in_days": 5, "price": 100, "features": ["Logo Design", "Visitenkarte"], "offer_type": "basic"},
                {"title": "Standard Design", "revisions": 5, "delivery_time_in_days": 7, "price": 200, "features": ["Logo Design", "Visitenkarte", "Briefpapier"], "offer_type": "standard"},
                {"title": "Premium Design", "revisions": 10, "delivery_time_in_days": 10, "price": 500, "features": ["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"], "offer_type": "premium"},
            ],
        }

        response = self.client.post(url, offer_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_offer_403_fail_not_allowed(self):
        """Ensure creating an offer fails with an error 403 if the user is authenticated but not a business user."""

        url = reverse("offer-list")
        self.authenticate(self.customer_user)
        offer_data = {
            "title": "Grafikdesign-Paket",
            "image": None,
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {"title": "Basic Design", "revisions": 2, "delivery_time_in_days": 5, "price": 100, "features": ["Logo Design", "Visitenkarte"], "offer_type": "basic"},
                {"title": "Standard Design", "revisions": 5, "delivery_time_in_days": 7, "price": 200, "features": ["Logo Design", "Visitenkarte", "Briefpapier"], "offer_type": "standard"},
                {"title": "Premium Design", "revisions": 10, "delivery_time_in_days": 10, "price": 500, "features": ["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"], "offer_type": "premium"},
            ],
        }

        response = self.client.post(url, offer_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
