from django.contrib.auth.models import AbstractUser
from django.db import models

from rest_framework.authtoken.models import TokenProxy


class CustomUser(AbstractUser):
    """Custom user model extending Django's AbstractUser to include a user type field."""

    email = models.EmailField(unique=True)
    USER_TYPE_CHOICES = (
        ("customer", "Customer"),
        ("business", "Business"),
    )
    type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.get_type_display()})"


class CustomToken(TokenProxy):
    """Custom proxy model for the Token model to allow for customization in the Django admin interface."""

    class Meta:
        proxy = True
        verbose_name = "Token"
        verbose_name_plural = "Tokens"
