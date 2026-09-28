from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from profiles_app.api.permissions import IsProfileOwnerOrReadOnly
from profiles_app.api.serializers import ProfileDetailSerializer, BusinessProfileListSerializer, CustomerProfileListSerializer
from profiles_app.models import Profile


class ProfileViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    ViewSet for handling profile-related operations, including retrieving and updating profiles, as well as listing business and customer profiles.
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer
    permission_classes = [IsAuthenticated, IsProfileOwnerOrReadOnly]

    def get_serializer_class(self):
        """Return the appropriate serializer class based on the action being performed."""
        if self.action == "business":
            return BusinessProfileListSerializer
        if self.action == "customer":
            return CustomerProfileListSerializer
        return ProfileDetailSerializer

    @action(detail=False, methods=["get"], url_path="business")
    def business(self, request):
        """Retrieve a list of business profiles."""
        business_profiles = self.get_queryset().filter(user__type="business")
        serializer = self.get_serializer(business_profiles, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="customer")
    def customer(self, request):
        """Retrieve a list of customer profiles."""
        customer_profiles = self.get_queryset().filter(user__type="customer")
        serializer = self.get_serializer(customer_profiles, many=True)
        return Response(serializer.data)
