from django.urls import reverse

from rest_framework import status
from rest_framework.fields import DateTimeField

from reviews_app.models import Review
from reviews_app.tests.base_review import BaseReviewTestCase


class ReviewListTests(BaseReviewTestCase):
    """Tests for listing reviews."""

    def setUp(self):
        """Set up the test environment by creating multiple reviews for testing the list functionality."""
        super().setUp()
        self.second_review = self.create_review(
            business_user=self.business_user2,
            reviewer=self.customer_user,
            rating=5,
            description="Sehr zufrieden mit dem Ergebnis.",
        )
        self.third_review = self.create_review(
            business_user=self.business_user,
            reviewer=self.empty_pf_user,
            rating=2,
            description="Das Ergebnis war ausbaufähig.",
        )
        self.fourth_review = self.create_review(
            business_user=self.business_user2,
            reviewer=self.empty_pf_user,
            rating=1,
            description="Leider nicht zufrieden.",
        )

    def test_list_reviews_200_success(self):
        """Ensure retrieving a list of reviews is successful and returns the expected fields."""

        url = reverse("review-list")
        self.authenticate(self.business_user)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_fields = {
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
        }

        for review_data in response.data:
            for field in expected_fields:
                self.assertIn(field, review_data)
            self.assertEqual(len(review_data), len(expected_fields))

        print(response.data)

    def test_list_reviews_401_fail_not_authenticated(self):
        """Ensure retrieving a list of reviews fails with an error 401 when the user is not authenticated."""
        url = reverse("review-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
