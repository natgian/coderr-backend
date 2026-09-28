from django.urls import path

from profiles_app.api.views import ProfileViewSet

urlpatterns = [
    path("profile/<int:pk>/", ProfileViewSet.as_view({"get": "retrieve", "patch": "partial_update"}), name="profile-detail"),
    path("profiles/business/", ProfileViewSet.as_view({"get": "business"}), name="profile-business"),
    path("profiles/customer/", ProfileViewSet.as_view({"get": "customer"}), name="profile-customer"),
]
