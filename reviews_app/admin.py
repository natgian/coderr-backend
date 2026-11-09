from django.contrib import admin

# Register your models here.

from reviews_app.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Configuration for the Review model in the Django admin interface."""

    list_display = ("id", "reviewer", "business_user", "rating", "created_at", "updated_at")
    list_display_links = ("id",)
