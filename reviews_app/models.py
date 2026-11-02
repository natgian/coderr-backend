from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings


class Review(models.Model):
    """Represents a review created by a customer user."""

    business_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_reviews")
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="written_reviews")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["reviewer", "business_user"], name="unique_reviewer_per_business")]

    def __str__(self):
        return f"#{self.id} by {self.reviewer} for {self.business_user}: {self.rating} Stars"
