from django import forms
from django_filters import rest_framework as filters

from reviews_app.models import Review


class IntegerFilter(filters.Filter):
    """
    Custom filter class for filtering integer fields.
    It uses Django's forms.IntegerField to handle integer input validation.
    """

    field_class = forms.IntegerField


class ReviewFilter(filters.FilterSet):
    """FilterSet for filtering reviews by business_user ID and reviewer ID."""

    business_user_id = IntegerFilter(
        field_name="business_user",
        min_value=1,
    )

    reviewer_id = IntegerFilter(
        field_name="reviewer",
        min_value=1,
    )

    class Meta:
        model = Review
        fields = []
