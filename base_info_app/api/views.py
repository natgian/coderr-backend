from django.db.models import Avg, Count

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from offers_app.models import Offer
from profiles_app.models import Profile
from reviews_app.models import Review


class BaseInfoView(APIView):
    """View to retrieve base information including review count, average rating, business profile count, and offer count."""

    permission_classes = [AllowAny]

    def get(self, request):
        """Get base info including review count, average rating, business profile count, and offer count."""
        reviews = Review.objects.aggregate(review_count=Count("id"), average_rating=Avg("rating", default=0.0))

        data = {
            "review_count": reviews["review_count"],
            "average_rating": round(reviews["average_rating"], 1),
            "business_profile_count": Profile.objects.filter(user__type="business").count(),
            "offer_count": Offer.objects.count(),
        }

        return Response(data)
