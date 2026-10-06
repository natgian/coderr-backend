from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status

from offers_app.api.serializers import OfferSerializer
from offers_app.models import Offer, OfferDetail

from test_utils.base_setup import BaseSetupTestCase

User = get_user_model()


class OfferDetailReadTests(BaseSetupTestCase):
    """Tests for retrieving offer details."""

    def test_list_offer_details_200_success(self):
        """Ensure that retrieving offer details returns a 200 OK status and the expected data."""
        url = reverse("offerdetail-detail", kwargs={"pk": self.detail_web_basic.pk})
        self.authenticate(self.business_user)

        response = self.client.get(url)

        expected_data = {
            "id": self.detail_web_basic.pk,
            "title": self.detail_web_basic.title,
            "revisions": self.detail_web_basic.revisions,
            "delivery_time_in_days": self.detail_web_basic.delivery_time_in_days,
            "price": self.detail_web_basic.price,
            "features": self.detail_web_basic.features,
            "offer_type": self.detail_web_basic.offer_type,
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_list_offer_details_401_fail_not_authenticated(self):
        """Ensure retrieving offer details fails with an error 401 if the user is not authenticated."""
        url = reverse("offerdetail-detail", kwargs={"pk": self.detail_web_basic.pk})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_offer_details_404_fail_not_found(self):
        """Ensure retrieving offer details fails with an error 404 if the offer detail does not exist."""
        url = reverse("offerdetail-detail", kwargs={"pk": 99999})
        self.authenticate(self.customer_user)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
