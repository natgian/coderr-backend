from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

from decimal import Decimal


class Offer(models.Model):
    """Represents an offer created by a business user, which can have multiple details associated with it."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="offers")
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="offers/", blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Offer {self.id}: {self.title}"


class OfferDetail(models.Model):
    """
    Represents the details of an offer, including title, revisions, delivery time, price, features, and offer type.
    """

    OFFER_TYPE_CHOICES = (
        ("basic", "Basic"),
        ("standard", "Standard"),
        ("premium", "Premium"),
    )

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="details")
    title = models.CharField(max_length=255)
    revisions = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(50)])
    delivery_time_in_days = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))])
    features = models.JSONField()
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPE_CHOICES, default="standard")

    def __str__(self):
        return f"{self.title} ({self.get_offer_type_display()})"
