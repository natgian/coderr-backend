from django.conf import settings
from django.db import models
from django.db.models import OneToOneField


class Profile(models.Model):
    """Model representing a user profile, linked to the user model via a one-to-one relationship."""

    user = OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150, blank=True, default="")
    last_name = models.CharField(max_length=150, blank=True, default="")
    file = models.ImageField(upload_to="uploads/", blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, default="")
    tel = models.CharField(max_length=30, blank=True, default="")
    description = models.TextField(blank=True, default="")
    working_hours = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip() or self.user.username
