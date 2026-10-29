from django.urls import reverse

from rest_framework import status

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
