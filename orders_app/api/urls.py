from django.urls import path, include
from rest_framework.routers import DefaultRouter

from orders_app.api.views import OrderCountView, OrderViewSet

router = DefaultRouter()
router.register(r"orders", OrderViewSet, basename="order")

urlpatterns = [
    path("", include(router.urls)),
    path("order-count/<int:business_user_id>/", OrderCountView.as_view(), name="order-count"),
]
