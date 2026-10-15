from rest_framework.pagination import PageNumberPagination


class OffersPagination(PageNumberPagination):
    """Custom pagination class for offers, allowing users to specify the page size through a query parameter."""

    page_size = 6
    page_size_query_param = "page_size"
    max_page_size = 100
