from reviews_app.models import Review

from test_utils.base_setup import BaseSetupTestCase


class BaseReviewTestCase(BaseSetupTestCase):
    """Base test case for review-related tests."""

    def setUp(self):
        """Set up initial data for review-related tests, including creating a default review for testing purposes."""
        super().setUp()
        self.review = Review.objects.create(
            business_user=self.business_user,
            reviewer=self.customer_user,
            rating=4,
            description="Bester Service!",
        )

    def create_review(self, business_user, reviewer, rating, description):
        """Create a review with the specified business_user, reviewer, rating and description."""

        return Review.objects.create(business_user=business_user, reviewer=reviewer, rating=rating, description=description)
