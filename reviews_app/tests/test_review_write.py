from django.urls import reverse

from rest_framework import status
from rest_framework.fields import DateTimeField

from reviews_app.models import Review

from test_utils.base_setup import BaseSetupTestCase


class ReviewCreateTests(BaseSetupTestCase):
    """Tests for creating a review."""

    def setUp(self):
        super().setUp()
        self.review = Review.objects.create(
            business_user=self.business_user,
            reviewer=self.customer_user,
            rating=5,
            description="Bester Service!",
        )

    def test_create_review_201_success(self):
        """Ensure creating a review succeeds with a 201 and returns the correct data."""

        url = reverse("review-list")
        initial_count = Review.objects.count()
        self.authenticate(self.empty_pf_user)

        review_data = {"business_user": self.business_user.pk, "rating": 4, "description": "Alles war toll!"}

        response = self.client.post(url, review_data, format="json")

        # response status assertion
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # database assertions
        self.assertEqual(Review.objects.count(), initial_count + 1)

        created_review = Review.objects.get(pk=response.data["id"])

        self.assertEqual(created_review.business_user, self.business_user)
        self.assertEqual(created_review.reviewer, self.empty_pf_user)
        self.assertEqual(created_review.rating, review_data["rating"])
        self.assertEqual(created_review.description, review_data["description"])

        # response data assertions
        expected_data = {
            "id": created_review.pk,
            "business_user": self.business_user.pk,
            "reviewer": self.empty_pf_user.pk,
            "rating": review_data["rating"],
            "description": review_data["description"],
            "created_at": DateTimeField().to_representation(created_review.created_at),
            "updated_at": DateTimeField().to_representation(created_review.updated_at),
        }

        self.assertEqual(response.data, expected_data)

    def test_create_review_400_fail_business_already_reviewed(self):
        """
        Ensure creating a review fails with an error 400 when a reviewer has already left a review for the same business user.
        """
        url = reverse("review-list")
        initial_count = Review.objects.count()
        self.authenticate(self.customer_user)

        review_data = {"business_user": self.business_user.pk, "rating": 4, "description": "Alles war toll!"}

        response = self.client.post(url, review_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Review.objects.count(), initial_count)

    def test_create_review_400_fail_invalid_data(self):
        """Ensure creating a review fails with an error 400 if the provided data is invalid."""

        url = reverse("review-list")
        initial_count = Review.objects.count()
        self.authenticate(self.empty_pf_user)

        valid_data = {
            "business_user": self.business_user.pk,
            "rating": 4,
            "description": "Alles war toll!",
        }

        invalid_cases = [
            ("business_user", "abc"),
            ("rating", "abc"),
            ("rating", -3),
            ("rating", 0),
            ("rating", 6),
            ("description", ""),
            ("description", None),
            ("description", []),
        ]

        for field, value in invalid_cases:
            with self.subTest(field=field, value=value):
                review_data = {**valid_data, field: value}

                response = self.client.post(url, review_data, format="json")

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(Review.objects.count(), initial_count)

    def test_create_review_400_fail_missing_field(self):
        """Ensure creating a review fails with an error 400 if any required field is missing."""
        url = reverse("review-list")
        initial_count = Review.objects.count()
        self.authenticate(self.empty_pf_user)

        valid_data = {
            "business_user": self.business_user.pk,
            "rating": 4,
            "description": "Alles war toll!",
        }

        for field in ("business_user", "rating", "description"):
            with self.subTest(missing_field=field):
                review_data = valid_data.copy()
                del review_data[field]

                response = self.client.post(url, review_data, format="json")

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(Review.objects.count(), initial_count)

    def test_create_review_400_fail_business_user_not_type_business(self):
        """Ensure creating a review fails with an error 400 if the business_user is not of type "business"."""
        url = reverse("review-list")
        initial_count = Review.objects.count()
        self.authenticate(self.empty_pf_user)

        review_data = {"business_user": self.customer_user.pk, "rating": 4, "description": "Alles war toll!"}

        response = self.client.post(url, review_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Review.objects.count(), initial_count)

    def test_create_review_401_fail_not_authenticated(self):
        """Ensure creating a review fails with an error 401 if the user is not authenticated."""
        url = reverse("review-list")
        review_data = {"business_user": self.business_user.pk, "rating": 4, "description": "Alles war toll!"}

        response = self.client.post(url, review_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_review_403_fail_not_customer_user(self):
        """Ensure creating a review fails with an error 403 if the authenticated user is not a customer user."""
        url = reverse("review-list")
        self.authenticate(self.business_user2)

        review_data = {"business_user": self.business_user.pk, "rating": 4, "description": "Alles war toll!"}

        response = self.client.post(url, review_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
