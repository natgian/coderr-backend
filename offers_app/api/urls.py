from django.urls import path, include
from rest_framework.routers import DefaultRouter

from offers_app.api.views import OfferDetailView, OfferViewSet

router = DefaultRouter()
router.register(r"offers", OfferViewSet, basename="offer")

urlpatterns = [
    path("", include(router.urls)),
    path("offerdetails/<int:pk>/", OfferDetailView.as_view(), name="offerdetail-detail"),
]
