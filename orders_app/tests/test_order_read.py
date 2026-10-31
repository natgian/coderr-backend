from django.urls import reverse

from rest_framework import status

from orders_app.models import Order
from orders_app.tests.base_order import BaseOrderTestCase


class OrderListTests(BaseOrderTestCase):
    """Tests for listing orders."""

    def setUp(self):
        """Set up initial data for order list tests, including creating orders for different users."""
        super().setUp()
        self.other_customer_order = self.create_order(self.detail_social_premium, self.empty_pf_user)

    def test_list_own_orders_customer_user_200_success(self):
        """Ensure listings orders returns only the orders belonging to the authenticated customer user with a 200 status code."""
        url = reverse("order-list")

        cases = [
            (self.customer_user, self.order),
            (self.empty_pf_user, self.other_customer_order),
        ]

        for user, own_order in cases:
            with self.subTest(user=user):
                self.authenticate(user)

                response = self.client.get(url)

                self.assertEqual(response.status_code, status.HTTP_200_OK)

                returned_ids = set()
                for order in response.data:
                    returned_ids.add(order["id"])

                self.assertEqual(returned_ids, {own_order.pk})

    def test_list_own_orders_business_user_200_success(self):
        """Ensure listings orders returns only the orders belonging to the authenticated business user with a 200 status code."""
        url = reverse("order-list")

        cases = [
            (self.business_user, self.order),
            (self.business_user2, self.other_customer_order),
        ]

        for user, own_order in cases:
            with self.subTest(user=user):
                self.authenticate(user)

                response = self.client.get(url)

                self.assertEqual(response.status_code, status.HTTP_200_OK)

                returned_ids = set()
                for order in response.data:
                    returned_ids.add(order["id"])

                self.assertEqual(returned_ids, {own_order.pk})

    def test_list_orders_401_fail_not_authenticated(self):
        """Ensure listings orders fails with an error 401 if the user is not authenticated."""

        url = reverse("order-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class OrderCountTests(BaseOrderTestCase):
    """Tests for counting orders for a specific business user."""

    def setUp(self):
        """Set up initial data for order count tests, including creating multiple orders for different users and statuses."""
        super().setUp()
        self.second_oder_in_progress = self.create_order(self.detail_graphic_premium, self.customer_user)
        self.third_order_completed = self.create_order(self.detail_web_standard, self.customer_user, "completed")

    def test_get_business_user_in_progress_order_count_200_success(self):
        """Ensure getting the order count for a business user returns the correct count of in-progress orders with a 200 status code."""
        self.authenticate(self.customer_user)

        cases = [
            (self.business_user.pk, 2),
            (self.business_user2.pk, 0),
        ]

        for business_user_id, expected_count in cases:
            url = reverse("order-count", kwargs={"business_user_id": business_user_id})

            response = self.client.get(url)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, {"order_count": expected_count})

    def test_get_business_user_in_progress_order_count_401_fail_not_authenticated(self):
        """Ensure getting the order count for a business user fails with an error 401 if the user is not authenticated."""
        url = reverse("order-count", kwargs={"business_user_id": self.business_user.pk})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_business_user_in_progress_order_count_404_fail_not_found(self):
        """Ensure getting the order count for a business user fails with an error 404 if the user does not exist."""
        url = reverse("order-count", kwargs={"business_user_id": 99999})
        self.authenticate(self.customer_user)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_business_user_completed_order_count_200_success(self):
        """Ensure getting the completed order count for a business user returns the correct count of completed orders with a 200 status code."""
        self.authenticate(self.customer_user)

        cases = [
            (self.business_user.pk, 1),
            (self.business_user2.pk, 0),
        ]

        for business_user_id, expected_count in cases:
            url = reverse("completed-order-count", kwargs={"business_user_id": business_user_id})

            response = self.client.get(url)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, {"completed_order_count": expected_count})
