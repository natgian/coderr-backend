from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from rest_framework.authtoken.admin import TokenAdmin
from rest_framework.authtoken.models import TokenProxy

from users_app.models import CustomUser, CustomToken


class CustomerUserAdmin(UserAdmin):
    """Configuration for the Django admin interface for the CustomUser model."""

    list_display = (
        "id",
        "username",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    list_filter = ("is_active", "is_staff", "is_superuser")


# Unregister the original model from the section in the Django Admin Panel.
try:
    admin.site.unregister(TokenProxy)
except admin.sites.NotRegistered:
    pass

admin.site.register(CustomToken, TokenAdmin)

# Register the custom proxy token model under the User Management section in the Django Admin Panel.
admin.site.register(CustomUser, CustomerUserAdmin)
