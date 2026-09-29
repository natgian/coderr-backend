from django.contrib import admin

from offers_app.models import Offer, OfferDetail


class OfferDetailInline(admin.StackedInline):
    model = OfferDetail
    extra = 3
    max_num = 3


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user")
    inlines = [OfferDetailInline]
