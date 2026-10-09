from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.fields import DateTimeField

from offers_app.models import Offer

from test_utils.base_setup import BaseSetupTestCase

User = get_user_model()


class OfferDetailReadTests(BaseSetupTestCase):
    """Tests for retrieving offer details."""

    def test_list_offer_details_200_success(self):
        """Ensure that retrieving offer details returns a 200 OK status and the expected data."""
        url = reverse("offerdetail-detail", kwargs={"pk": self.detail_web_basic.pk})
        self.authenticate(self.business_user)

        expected_data = {
            "id": self.detail_web_basic.pk,
            "title": self.detail_web_basic.title,
            "revisions": self.detail_web_basic.revisions,
            "delivery_time_in_days": self.detail_web_basic.delivery_time_in_days,
            "price": self.detail_web_basic.price,
            "features": self.detail_web_basic.features,
            "offer_type": self.detail_web_basic.offer_type,
        }

        response = self.client.get(url)

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


class OfferListTests(BaseSetupTestCase):
    """
    Tests for retrieving the list of offers, including annotated minimum price and delivery time for each offer.
    """

    def test_list_offers_200_success(self):
        """
        Ensure that retrieving the list of offers returns a 200 OK status and the expected data, including annotated minimum price and delivery time for each offer.
        """
        url = reverse("offer-list")
        offer_count = Offer.objects.count()

        details = [self.detail_web_basic, self.detail_web_standard, self.detail_web_premium]

        expected_min_price = min(detail.price for detail in details)
        expected_min_delivery_time = min(detail.delivery_time_in_days for detail in details)

        expected_details = []
        for detail in details:
            expected_details.append(
                {
                    "id": detail.id,
                    "url": f"http://testserver/api/offerdetails/{detail.id}/",
                }
            )

        expected_offer_data = {
            "id": self.offer_web.pk,
            "user": self.business_user.pk,
            "title": self.offer_web.title,
            "image": None,
            "description": self.offer_web.description,
            "created_at": DateTimeField().to_representation(self.offer_web.created_at),
            "updated_at": DateTimeField().to_representation(self.offer_web.updated_at),
            "details": expected_details,
            "min_price": expected_min_price,
            "min_delivery_time": expected_min_delivery_time,
            "user_details": {
                "first_name": self.business_profile.first_name,
                "last_name": self.business_profile.last_name,
                "username": self.business_user.username,
            },
        }

        response = self.client.get(url, {"limit": offer_count})

        # response assertion
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # pagination assertions
        self.assertEqual(response.data["count"], offer_count)
        self.assertEqual(len(response.data["results"]), offer_count)
        self.assertIsNone(response.data["previous"])
        self.assertIsNone(response.data["next"])

        # listed offer assertions
        listed_offer = None

        for offer_data in response.data["results"]:
            if offer_data["id"] == self.offer_web.pk:
                listed_offer = offer_data
                break

        self.assertIsNotNone(listed_offer)
        self.assertEqual(listed_offer, expected_offer_data)
