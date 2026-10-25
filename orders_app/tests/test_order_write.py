from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.fields import DateTimeField

from orders_app.models import Order

from test_utils.base_setup import BaseSetupTestCase

User = get_user_model()


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


class BaseOrderTestCase(BaseSetupTestCase):
    """Base test case for order-related tests."""

    def setUp(self):
        super().setUp()
        offer_detail = self.detail_web_basic

        self.order = Order.objects.create(
            offer_detail=offer_detail,
            customer_user=self.customer_user,
            business_user=offer_detail.offer.user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
        )


class OrderUpdateTests(BaseOrderTestCase):
    """Tests for updating orders."""

    def test_update_order_200_success(self):
        """Ensure updating an order succeeds with a 200 and updates the order status correctly."""
        url = reverse("order-detail", kwargs={"pk": self.order.pk})
        self.authenticate(self.business_user)

        order_data = {"status": "completed"}

        response = self.client.patch(url, order_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "completed")

    def test_update_order_400_fail_invalid_data(self):
        """Ensure updating an order fails with an error 400 if the provided data is invalid."""
        url = reverse("order-detail", kwargs={"pk": self.order.pk})
        self.authenticate(self.business_user)

        invalid_cases = [
            ("status", "abc"),
            ("status", 123),
            ("abc", "completed"),
        ]

        for param, value in invalid_cases:
            with self.subTest(param=param, value=value):
                response = self.client.patch(url, {param: value})
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_order_401_fail_not_authenticated(self):
        """Ensure updating an order fails with an error 401 if the user is not authenticated."""
        url = reverse("order-detail", kwargs={"pk": self.order.pk})
        order_data = {"status": "completed"}

        response = self.client.patch(url, order_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_order_403_fail_not_business_user(self):
        """Ensure updating an order fails with an error 403 if the authenticated user is not a business user."""
        url = reverse("order-detail", kwargs={"pk": self.order.pk})
        self.authenticate(self.customer_user)

        order_data = {"status": "completed"}

        response = self.client.patch(url, order_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_order_404_fail_order_not_found(self):
        """Ensure updating an order fails with an error 404 if the specified order does not exist."""
        url = reverse("order-detail", kwargs={"pk": 99999})
        self.authenticate(self.business_user)

        order_data = {"status": "completed"}

        response = self.client.patch(url, order_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class OrderDeleteTests(BaseOrderTestCase):
    """Tests for deleting orders."""

    def setUp(self):
        """"""
        super().setUp()
        self.staff_user = User.objects.create_user(username="staffUser", email="staff@email.com", password="staffPassword", type="business", is_staff=True)

    def test_delete_order_204_success(self):
        """Ensure deleting an order succeeds with a 204 and removes the order from the database."""
        order_id = self.order.pk
        initial_order_count = Order.objects.count()

        url = reverse("order-detail", kwargs={"pk": self.order.pk})
        self.authenticate(self.staff_user)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(pk=order_id).exists())
        self.assertEqual(Order.objects.count(), initial_order_count - 1)

    def test_delete_order_401_fail_not_authenticated(self):
        """Ensure deleting an order fails with an error 401 if the user is not authenticated."""
        url = reverse("order-detail", kwargs={"pk": self.order.pk})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Order.objects.filter(pk=self.order.pk).exists())

    def test_delete_order_403_fail_not_staff_user(self):
        """Ensure deleting an order fails with an error 403 if the authenticated user is not a staff user."""
        url = reverse("order-detail", kwargs={"pk": self.order.pk})
        self.authenticate(self.business_user)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Order.objects.filter(pk=self.order.pk).exists())

    def test_delete_order_404_fail_order_not_found(self):
        """Ensure deleting an order fails with an error 404 if the specified order does not exist."""
        url = reverse("order-detail", kwargs={"pk": 99999})
        self.authenticate(self.staff_user)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
