from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class ProfileViewSet(viewsets.ModelViewSet):
    """"""

    permission_classes = [AllowAny]

    def retrieve(self, request, pk=None):
        return Response(
            {
                "id": pk,
                "mode": "dummy-detail",
            },
            status=status.HTTP_200_OK,
        )
