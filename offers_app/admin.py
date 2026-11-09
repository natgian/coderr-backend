from django.contrib import admin

from offers_app.models import Offer, OfferDetail


class OfferDetailInline(admin.StackedInline):
    """Configuration of the OfferDetail model in the admin panel."""

    model = OfferDetail
    extra = 3
    max_num = 3


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    """Configuration of the Offer model in the admin panel."""

    list_display = ("id", "title", "user")
    list_display_links = ("title",)
    inlines = [OfferDetailInline]
