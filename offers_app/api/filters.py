from django import forms
from django_filters import rest_framework as filters

from offers_app.models import Offer


class IntegerFilter(filters.Filter):
    """
    Custom filter class for filtering integer fields.
    It uses Django's forms.IntegerField to handle integer input validation.
    """

    field_class = forms.IntegerField


class FloatFilter(filters.Filter):
    """
    Custom filter class for filtering float fields.
    It uses Django's forms.FloatField to handle float input validation.
    """

    field_class = forms.FloatField


class OfferFilter(filters.FilterSet):
    """FilterSet for filtering offers by creator ID, minimum price and maximum delivery time."""

    creator_id = IntegerFilter(
        field_name="user_id",
        min_value=1,
    )

    min_price = FloatFilter(
        field_name="min_price",
        lookup_expr="gte",
        min_value=1.00,
    )

    max_delivery_time = IntegerFilter(
        field_name="min_delivery_time",
        lookup_expr="lte",
        min_value=1,
    )

    class Meta:
        model = Offer
        fields = []
