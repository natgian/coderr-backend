from django.urls import reverse

from rest_framework import status

from reviews_app.models import Review
from test_utils.base_setup import BaseSetupTestCase


class BaseInfoTests(BaseSetupTestCase):
    """
    Test cases for the BaseInfoView API endpoint, which retrieves base information including review count, average rating, business profile count and offer count.
    """

    def test_list_base_info_200_success(self):
        """Ensure that the BaseInfoView API endpoint returns the correct base information with a 200 OK status."""
        Review.objects.create(
            business_user=self.business_user,
            reviewer=self.customer_user,
            rating=5,
            description="Sehr zufrieden!",
        )
        Review.objects.create(
            business_user=self.business_user2,
            reviewer=self.customer_user,
            rating=2,
            description="Nicht zufrieden.",
        )

        url = reverse("base-info")

        response = self.client.get(url)

        expected_data = {
            "review_count": 2,
            "average_rating": 3.5,
            "business_profile_count": 2,
            "offer_count": 3,
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_base_info_without_reviews(self):
        """Ensure that the BaseInfoView API endpoint returns the correct base information with a 200 OK status when there are no reviews."""
        url = reverse("base-info")

        response = self.client.get(url)

        expected_data = {
            "review_count": 0,
            "average_rating": 0.0,
            "business_profile_count": 2,
            "offer_count": 3,
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
