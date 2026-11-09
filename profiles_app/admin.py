from django.contrib import admin

from profiles_app.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Configuration for the Profile model in the Django admin interface."""

    list_display = ("id", "user", "first_name", "last_name", "user__email")
    list_display_links = ("id", "user")
