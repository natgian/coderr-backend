from django.contrib import admin

from orders_app.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Configuration for the Order model in the Django admin interface."""

    list_display = ("id", "title", "customer_user", "business_user", "status")
    list_display_links = ("id", "title")
