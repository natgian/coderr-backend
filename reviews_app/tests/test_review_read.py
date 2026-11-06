from datetime import timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from rest_framework import status

from reviews_app.models import Review
from reviews_app.tests.base_review import BaseReviewTestCase

User = get_user_model()


class BaseReviewListTestCase(BaseReviewTestCase):
    def setUp(self):
        """Set up the test environment by creating multiple reviews for testing the list functionality."""
        super().setUp()

        self.test_reviewer = User.objects.create_user(
            username="testReviewer",
            email="testReviewer@mail.com",
            password="testReviewer",
            type="customer",
        )

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
        self.fifth_review = self.create_review(
            business_user=self.business_user,
            reviewer=self.test_reviewer,
            rating=3,
            description="Gute Arbeit, mit etwas Luft nach oben.",
        )


class ReviewListTests(BaseReviewListTestCase):
    """Tests for listing reviews."""

    def test_list_reviews_200_success(self):
        """Ensure retrieving a list of reviews is successful and returns the expected fields."""

        url = reverse("review-list")
        self.authenticate(self.business_user)

        response = self.client.get(url)

        # response assertions
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

        # count assertion
        expected_count = Review.objects.count()
        self.assertEqual(len(response.data), expected_count)

    def test_list_reviews_401_fail_not_authenticated(self):
        """Ensure retrieving a list of reviews fails with an error 401 when the user is not authenticated."""
        url = reverse("review-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ReviewListFilterTests(BaseReviewListTestCase):
    """Tests for filtering the list of reviews based on business_user ID or reviewer ID."""

    def test_filter_reviews_by_business_user_id(self):
        """Ensure filtering reviews by business_user ID returns the expected reviews."""
        url = reverse("review-list")
        self.authenticate(self.customer_user)

        expected_reviews = Review.objects.filter(business_user=self.business_user.pk)

        response = self.client.get(url, {"business_user_id": self.business_user.pk})

        # response assertion
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # filter assertions
        result_ids = []
        for review in response.data:
            result_ids.append(review["id"])

        expected_ids = []
        for review in expected_reviews:
            expected_ids.append(review.id)

        self.assertCountEqual(result_ids, expected_ids)

    def test_filter_reviews_by_reviewer_id(self):
        """Ensure filtering reviews by reviewer ID returns the expected reviews."""

        url = reverse("review-list")
        self.authenticate(self.customer_user)

        expected_reviews = Review.objects.filter(reviewer=self.test_reviewer.pk)

        response = self.client.get(url, {"reviewer_id": self.test_reviewer.pk})

        # response assertion
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # filter assertions
        result_ids = []
        for review in response.data:
            result_ids.append(review["id"])

        expected_ids = []
        for review in expected_reviews:
            expected_ids.append(review.id)

        self.assertCountEqual(result_ids, expected_ids)

    def test_filter_reviews_by_business_user_and_reviewer_ids(self):
        """Ensure filtering reviews by business_user and reviewer IDs returns the expected reviews."""
        url = reverse("review-list")
        self.authenticate(self.customer_user)

        expected_reviews = Review.objects.filter(reviewer=self.customer_user.pk, business_user=self.business_user)

        response = self.client.get(url, {"reviewer_id": self.customer_user.pk, "business_user_id": self.business_user.pk})

        # response assertion
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # filter assertions
        result_ids = []
        for review in response.data:
            result_ids.append(review["id"])

        expected_ids = []
        for review in expected_reviews:
            expected_ids.append(review.id)

        self.assertCountEqual(result_ids, expected_ids)

    def test_filter_reviews_400_fail_invalid_data(self):
        """Ensure filtering reviews with invalid data fails with an error 400."""
        url = reverse("review-list")
        self.authenticate(self.customer_user)

        invalid_cases = [
            ("business_user_id", "abc"),
            ("business_user_id", 0),
            ("business_user_id", -5),
            ("reviewer_id", "abc"),
            ("reviewer_id", 0),
            ("reviewer_id", -5),
        ]

        for param, value in invalid_cases:
            with self.subTest(param=param, value=value):
                response = self.client.get(url, {param: value})
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ReviewListOrderingTests(BaseReviewListTestCase):
    """"""

    def setUp(self):
        """"""
        super().setUp()
        now = timezone.now()

        Review.objects.filter(pk=self.review.pk).update(
            created_at=now - timedelta(days=14),
            updated_at=now - timedelta(days=8),
        )
        Review.objects.filter(pk=self.second_review.pk).update(
            created_at=now - timedelta(days=10),
            updated_at=now - timedelta(days=5),
        )
        Review.objects.filter(pk=self.third_review.pk).update(
            created_at=now - timedelta(days=6),
            updated_at=now - timedelta(days=3),
        )
        Review.objects.filter(pk=self.fourth_review.pk).update(
            created_at=now - timedelta(days=4),
            updated_at=now - timedelta(days=1),
        )
        Review.objects.filter(pk=self.fifth_review.pk).update(
            created_at=now - timedelta(days=2),
            updated_at=now,
        )

    def test_ordering_reviews_by_updated_at(self):
        """Ensure that reviews can be ordered by the "updated_at" field in both ascending and descending order."""
        url = reverse("review-list")
        self.authenticate(self.customer_user)

        test_cases = [("updated_at", False), ("-updated_at", True)]

        for param, reverse_flag in test_cases:
            with self.subTest(param=param):
                response = self.client.get(url, {"ordering": param})

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(len(response.data), Review.objects.count())

                dates = []
                for review in response.data:
                    dates.append(review["updated_at"])

                direction = "descending" if reverse_flag else "ascending"
                error_msg = f"The reviews should be sorted {direction}"

                self.assertEqual(dates, sorted(dates, reverse=reverse_flag), msg=error_msg)

    def test_ordering_reviews_by_rating(self):
        """Ensure that reviews can be ordered by the "rating" field in both ascending and descending order."""
        url = reverse("review-list")
        self.authenticate(self.customer_user)

        test_cases = [("rating", False), ("-rating", True)]

        for param, reverse_flag in test_cases:
            with self.subTest(param=param):
                response = self.client.get(url, {"ordering": param})

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(len(response.data), Review.objects.count())

                ratings = []
                for review in response.data:
                    ratings.append(review["rating"])

                direction = "descending" if reverse_flag else "ascending"
                error_msg = f"The reviews should be sorted {direction}"

                self.assertEqual(ratings, sorted(ratings, reverse=reverse_flag), msg=error_msg)
