from orders_app.models import Order

from test_utils.base_setup import BaseSetupTestCase


class BaseOrderTestCase(BaseSetupTestCase):
    """Base test case for order-related tests."""

    def setUp(self):
        """Set up initial data for order-related tests, including creating a default order for testing purposes."""
        super().setUp()
        self.order = self.create_order(self.detail_web_basic, self.customer_user)

    def create_order(self, offer_detail, customer, status="in_progress"):
        """Create an order with the specified offer detail, customer, and status."""
        return Order.objects.create(
            offer_detail=offer_detail,
            customer_user=customer,
            business_user=offer_detail.offer.user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
            status=status,
        )
