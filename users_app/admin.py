from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users_app.models import CustomUser


class CustomerUserAdmin(UserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    list_filter = ("is_active", "is_staff", "is_superuser")


admin.site.register(CustomUser, CustomerUserAdmin)
