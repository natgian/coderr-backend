from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from profiles_app.api.permissions import IsProfileOwnerOrReadOnly
from profiles_app.api.serializers import ProfileSerializer
from profiles_app.models import Profile


class ProfileViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """ViewSet for handling profile retrieval and updates."""

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsProfileOwnerOrReadOnly]
