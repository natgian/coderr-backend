from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Custom user model extending Django's AbstractUser to include a user type field."""

    USER_TYPE_CHOICES = (
        ("customer", "Customer"),
        ("business", "Business"),
    )

    type = models.CharField(
        max_length=50, choices=USER_TYPE_CHOICES, default="customer"
    )
