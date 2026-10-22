from django.urls import reverse

from rest_framework import status
from rest_framework.fields import DateTimeField

from orders_app.models import Order

from test_utils.base_setup import BaseSetupTestCase


class OrderCreateTests(BaseSetupTestCase):
    """Tests for creating orders."""

    def test_create_order_201_success(self):
        """Ensure creating an order succeeds with a 201 and returns the correct data."""

        url = reverse("order-list")
        initial_order_count = Order.objects.count()
        self.authenticate(self.customer_user)

        offer_data = {"offer_detail_id": self.detail_graphic_basic.pk}

        response = self.client.post(url, offer_data, format="json")

        # response status assertion
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # database assertions
        self.assertEqual(Order.objects.count(), initial_order_count + 1)
        created_order = Order.objects.get(pk=response.data["id"])
        self.assertEqual(created_order.offer_detail, self.detail_graphic_basic)

        # users and order status assertions
        self.assertEqual(response.data["customer_user"], self.customer_user.pk)
        self.assertEqual(response.data["business_user"], self.business_user.pk)
        self.assertEqual(response.data["status"], "in_progress")

        # offer detail assertions
        expected_offerdetail_data = {
            "title": self.detail_graphic_basic.title,
            "revisions": self.detail_graphic_basic.revisions,
            "delivery_time_in_days": self.detail_graphic_basic.delivery_time_in_days,
            "price": self.detail_graphic_basic.price,
            "features": self.detail_graphic_basic.features,
            "offer_type": self.detail_graphic_basic.offer_type,
        }

        for field in expected_offerdetail_data:
            self.assertEqual(response.data[field], expected_offerdetail_data[field])
            self.assertEqual(getattr(created_order, field), expected_offerdetail_data[field])

        # dynamic date fields assertions
        self.assertEqual(response.data["created_at"], DateTimeField().to_representation(created_order.created_at))
        self.assertEqual(response.data["updated_at"], DateTimeField().to_representation(created_order.updated_at))

        # structure assertions
        self.assertNotIn("offer_detail", response.data)
        expected_fields_count = 12
        self.assertEqual(len(response.data), expected_fields_count)

    def test_create_order_400_fail_invalid_data(self):
        """Ensure creating an order fails with an error 400 if the provided data is invalid."""

        url = reverse("order-list")
        self.authenticate(self.customer_user)

        invalid_cases = [
            ("invalid data type", {"offer_detail_id": "abc"}),
            ("missing ID", {}),
            ("empty String", {"offer_detail_id": ""}),
        ]

        for case, offer_data in invalid_cases:
            with self.subTest(case=case):
                response = self.client.post(url, offer_data, format="json")
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_401_fail_not_authenticated(self):
        """Ensure creating an order fails with an error 401 if the user is not authenticated."""

        url = reverse("order-list")

        offer_data = {"offer_detail_id": self.detail_graphic_basic.pk}

        response = self.client.post(url, offer_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order_403_fail_not_customer_user(self):
        """Ensure creating an order fails with an error 403 if the authenticated user is not a customer user."""
        url = reverse("order-list")
        self.authenticate(self.business_user2)

        offer_data = {"offer_detail_id": self.detail_graphic_basic.pk}

        response = self.client.post(url, offer_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_order_404_fail_offer_detail_not_found(self):
        """Ensure creating an order fails with an error 404 if the provided offer_detail_id does not exist."""
        url = reverse("order-list")
        self.authenticate(self.customer_user)

        offer_data = {"offer_detail_id": 99999}

        response = self.client.post(url, offer_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
