from traceback import format_tb

from django.urls import reverse

from rest_framework import status
from rest_framework.fields import DateTimeField

from reviews_app.models import Review
from reviews_app.tests.base_review import BaseReviewTestCase

from test_utils.base_setup import BaseSetupTestCase


class ReviewCreateTests(BaseReviewTestCase):
    """Tests for creating a review."""

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


class ReviewUpdateTests(BaseReviewTestCase):
    """Tests for updating a review."""

    def test_update_review_rating_200_success(self):
        """Ensure updating a review's rating succeeds with a 200 and returns the correct data."""
        url = reverse("review-detail", kwargs={"pk": self.review.pk})
        self.authenticate(self.customer_user)
        original_description = self.review.description

        updated_data = {"rating": 5}

        response = self.client.patch(url, updated_data, format="json")

        # response status assertion
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # database assertions
        self.review.refresh_from_db()
        self.assertEqual(self.review.rating, updated_data["rating"])
        self.assertEqual(self.review.description, original_description)

        # response data assertions
        expected_data = {
            "id": self.review.pk,
            "business_user": self.review.business_user.pk,
            "reviewer": self.review.reviewer.pk,
            "rating": self.review.rating,
            "description": self.review.description,
            "created_at": DateTimeField().to_representation(self.review.created_at),
            "updated_at": DateTimeField().to_representation(self.review.updated_at),
        }

        self.assertEqual(response.data, expected_data)

    def test_update_review_description_200_success(self):
        """Ensure updating a review's description succeeds with a 200 and returns the correct data."""
        url = reverse("review-detail", kwargs={"pk": self.review.pk})
        self.authenticate(self.customer_user)

        updated_data = {"description": "UDATED: Der Service war super!"}

        response = self.client.patch(url, updated_data, format="json")

        # response status assertion
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # database assertions
        self.review.refresh_from_db()
        self.assertEqual(self.review.description, updated_data["description"])

        # response data assertions
        self.assertEqual(response.data["description"], updated_data["description"])

    def test_update_review_rating_and_description_200_success(self):
        """Ensure updating both a review's rating and description succeeds with a 200 and returns the correct data."""
        url = reverse("review-detail", kwargs={"pk": self.review.pk})
        self.authenticate(self.customer_user)

        updated_data = {"rating": 5, "description": "UPDATED: Der Service war super!"}

        response = self.client.patch(url, updated_data, format="json")

        # response status assertion
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # database assertions
        self.review.refresh_from_db()
        self.assertEqual(self.review.rating, updated_data["rating"])
        self.assertEqual(self.review.description, updated_data["description"])

        # response data assertions
        self.assertEqual(response.data["rating"], updated_data["rating"])
        self.assertEqual(response.data["description"], updated_data["description"])

    def test_update_review_400_fail_invalid_data(self):
        """Ensure updating a review fails with an error 400 if the provided data is invalid."""
        url = reverse("review-detail", kwargs={"pk": self.review.pk})
        self.authenticate(self.customer_user)
        original_rating = self.review.rating
        original_description = self.review.description

        updated_data = {"rating": "abc", "description": "UPDATED: Der Service war super!"}

        response = self.client.patch(url, updated_data, format="json")

        # response assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("rating", response.data)

        # database assertions
        self.review.refresh_from_db()
        self.assertEqual(self.review.rating, original_rating)
        self.assertEqual(self.review.description, original_description)

    def test_update_review_400_fail_business_user_change(self):
        """Ensure updating a review fails with an error 400 if the business_user is attempted to be changed."""
        url = reverse("review-detail", kwargs={"pk": self.review.pk})
        self.authenticate(self.customer_user)
        original_business_user = self.review.business_user
        original_rating = self.review.rating
        original_description = self.review.description

        updated_data = {"business_user": self.business_user2.pk, "rating": 5, "description": "UPDATED: Der Service war super!"}

        response = self.client.patch(url, updated_data, format="json")

        # response assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("business_user", response.data)

        # database assertions
        self.review.refresh_from_db()
        self.assertEqual(self.review.business_user, original_business_user)
        self.assertEqual(self.review.rating, original_rating)
        self.assertEqual(self.review.description, original_description)

    def test_update_review_401_fail_not_authenticated(self):
        """Ensure updating a review fails with an error 401 if the user is not authenticated."""
        url = reverse("review-detail", kwargs={"pk": self.review.pk})

        updated_data = {"rating": 1}

        response = self.client.patch(url, updated_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_review_403_fail_not_authorized(self):
        """Ensure updating a review fails with an error 403 if the authenticated user is not the creator of the review."""
        url = reverse("review-detail", kwargs={"pk": self.review.pk})
        self.authenticate(self.empty_pf_user)

        updated_data = {"rating": 1}

        response = self.client.patch(url, updated_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_review_404_fail_review_not_found(self):
        """Ensure updating a review fails with an error 404 if the review does not exist."""
        url = reverse("review-detail", kwargs={"pk": 99999})
        self.authenticate(self.customer_user)

        updated_data = {"rating": 1}

        response = self.client.patch(url, updated_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
