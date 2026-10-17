from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

from decimal import Decimal


class Order(models.Model):
    """Represents an order created by a customer user."""

    OFFER_TYPE_CHOICES = (
        ("basic", "Basic"),
        ("standard", "Standard"),
        ("premium", "Premium"),
    )

    ORDER_STATUS_CHOICES = (
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )

    offer_detail = models.ForeignKey("offers_app.OfferDetail", on_delete=models.SET_NULL, null=True, related_name="orders")  # if the offer is deleted, the order remains intact thanks to SET_NULL
    customer_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="placed_orders")
    business_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_orders")
    title = models.CharField(max_length=255)
    revisions = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(50)])
    delivery_time_in_days = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))])
    features = models.JSONField()
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPE_CHOICES, default="standard")
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default="in_progress")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id}: {self.title} ({self.get_status_display()})"
