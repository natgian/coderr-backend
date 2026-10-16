from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.fields import DateTimeField

from offers_app.models import Offer

from test_utils.base_setup import BaseSetupTestCase


class OfferDetailReadTests(BaseSetupTestCase):
    """Tests for retrieving offer details."""

    def test_retrieve_offer_details_200_success(self):
        """Ensure that retrieving offer details returns a 200 OK status and the expected data."""
        url = reverse("offerdetail-detail", kwargs={"pk": self.detail_web_basic.pk})
        self.authenticate(self.business_user)

        expected_data = {
            "id": self.detail_web_basic.pk,
            "title": self.detail_web_basic.title,
            "revisions": self.detail_web_basic.revisions,
            "delivery_time_in_days": self.detail_web_basic.delivery_time_in_days,
            "price": self.detail_web_basic.price,
            "features": self.detail_web_basic.features,
            "offer_type": self.detail_web_basic.offer_type,
        }

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_retrieve_offer_details_401_fail_not_authenticated(self):
        """Ensure retrieving offer details fails with an error 401 if the user is not authenticated."""
        url = reverse("offerdetail-detail", kwargs={"pk": self.detail_web_basic.pk})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_offer_details_404_fail_not_found(self):
        """Ensure retrieving offer details fails with an error 404 if the offer detail does not exist."""
        url = reverse("offerdetail-detail", kwargs={"pk": 99999})
        self.authenticate(self.customer_user)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class OfferListTests(BaseSetupTestCase):
    """Tests for retrieving the list of offers, including annotated minimum price and delivery time for each offer."""

    def test_list_offers_200_success(self):
        """
        Ensure that retrieving the list of offers returns a 200 OK status and the expected data, including annotated minimum price and delivery time for each offer.
        """
        url = reverse("offer-list")
        offer_count = Offer.objects.count()

        details = [self.detail_web_basic, self.detail_web_standard, self.detail_web_premium]

        expected_min_price = min(detail.price for detail in details)
        expected_min_delivery_time = min(detail.delivery_time_in_days for detail in details)

        expected_details = []
        for detail in details:
            expected_details.append(
                {
                    "id": detail.id,
                    "url": f"http://testserver/api/offerdetails/{detail.id}/",
                }
            )

        expected_offer_data = {
            "id": self.offer_web.pk,
            "user": self.business_user.pk,
            "title": self.offer_web.title,
            "image": None,
            "description": self.offer_web.description,
            "created_at": DateTimeField().to_representation(self.offer_web.created_at),
            "updated_at": DateTimeField().to_representation(self.offer_web.updated_at),
            "details": expected_details,
            "min_price": expected_min_price,
            "min_delivery_time": expected_min_delivery_time,
            "user_details": {
                "first_name": self.business_profile.first_name,
                "last_name": self.business_profile.last_name,
                "username": self.business_user.username,
            },
        }

        response = self.client.get(url, {"page_size": offer_count})

        # response assertion
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # result count and pagination assertions
        self.assertEqual(response.data["count"], offer_count)
        self.assertEqual(len(response.data["results"]), offer_count)
        self.assertIsNone(response.data["previous"])
        self.assertIsNone(response.data["next"])

        # listed offer assertions
        listed_offer = None

        for offer_data in response.data["results"]:
            if offer_data["id"] == self.offer_web.pk:
                listed_offer = offer_data
                break

        self.assertIsNotNone(listed_offer)
        self.assertEqual(listed_offer, expected_offer_data)


class OfferListFilterTests(BaseSetupTestCase):
    """Tests for filtering the list of offers based on creator ID, minimum price and maximum delivery time."""

    def test_list_offers_filter_by_creator_id(self):
        """Ensure that filtering offers by creator ID returns the expected offers."""
        url = reverse("offer-list")

        expected_offers = Offer.objects.filter(user=self.business_user)
        expected_count = expected_offers.count()

        response = self.client.get(
            url,
            {
                "creator_id": self.business_user.pk,
                "page_size": expected_count,
            },
        )

        # response assertion
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # filter assertions
        self.assertEqual(response.data["count"], expected_count)
        self.assertEqual(len(response.data["results"]), expected_count)

        result_ids = []
        for offer in response.data["results"]:
            result_ids.append(offer["id"])

        expected_ids = []
        for offer in expected_offers:
            expected_ids.append(offer.id)

        self.assertCountEqual(result_ids, expected_ids)

    def test_list_offers_filter_by_min_price(self):
        """Ensure that filtering offers by minimum price returns the expected offers."""
        url = reverse("offer-list")
        min_price_param = 200.00

        expected_ids = []
        for offer in Offer.objects.prefetch_related("details"):
            prices = []
            for detail in offer.details.all():
                prices.append(detail.price)

            if prices and min(prices) >= min_price_param:
                expected_ids.append(offer.pk)

        expected_count = len(expected_ids)

        response = self.client.get(
            url,
            {
                "min_price": min_price_param,
                "page_size": expected_count,
            },
        )

        # response assertion
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # filter assertions
        result_ids = []
        for offer in response.data["results"]:
            result_ids.append(offer["id"])

        self.assertEqual(response.data["count"], expected_count)
        self.assertCountEqual(result_ids, expected_ids)

    def test_list_offers_filter_by_max_delivery_time(self):
        """Ensure that filtering offers by maximum delivery time returns the expected offers."""
        url = reverse("offer-list")
        max_delivery_time_param = 5

        expected_ids = []
        for offer in Offer.objects.prefetch_related("details"):
            delivery_times = []
            for detail in offer.details.all():
                delivery_times.append(detail.delivery_time_in_days)

            if delivery_times and min(delivery_times) <= max_delivery_time_param:
                expected_ids.append(offer.pk)

        expected_count = len(expected_ids)

        response = self.client.get(
            url,
            {
                "max_delivery_time": max_delivery_time_param,
                "page_size": expected_count,
            },
        )

        # response assertion
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # filter assertions
        result_ids = []
        for offer in response.data["results"]:
            result_ids.append(offer["id"])

        self.assertEqual(response.data["count"], expected_count)
        self.assertCountEqual(result_ids, expected_ids)

    def test_list_offers_invalid_filter_parameters(self):
        """
        Ensure listing offers returns an error 400 if the filter parameters are invalid.
        Checks for invalid creator_id, min_price, and max_delivery_time values.
        """
        url = reverse("offer-list")
        invalid_cases = [
            ("creator_id", "abc"),
            ("creator_id", 0),
            ("min_price", "abc"),
            ("min_price", -10),
            ("max_delivery_time", "abc"),
            ("max_delivery_time", 0),
            ("max_delivery_time", -5),
            ("max_delivery_time", 12.5),
        ]

        for param, value in invalid_cases:
            with self.subTest(param=param, value=value):
                response = self.client.get(url, {param: value})
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OfferListOrderingTests(BaseSetupTestCase):
    """
    Tests for ordering the list of offers based on minimum price and updated_at timestamp,
    ensuring that the offers are returned in the expected order for both ascending and descending cases.
    """

    def test_list_offers_ordering_by_min_price(self):
        """Ensure that ordering offers by minimum price returns the expected order of offers in ascending and descending order."""
        url = reverse("offer-list")
        offer_count = Offer.objects.count()
        test_cases = [("min_price", False), ("-min_price", True)]

        for param, reverse_flag in test_cases:
            with self.subTest(param=param):
                response = self.client.get(url, {"ordering": param, "page_size": offer_count})

                self.assertEqual(response.status_code, status.HTTP_200_OK)

                prices = []
                for offer in response.data["results"]:
                    prices.append(offer["min_price"])

                direction = "descending" if reverse_flag else "ascending"
                error_msg = f"The prices should be sorted {direction}"

                self.assertEqual(len(prices), offer_count, msg="The API did not return all the listings.")
                self.assertEqual(prices, sorted(prices, reverse=reverse_flag), msg=error_msg)

    def test_list_offers_ordering_by_updated_at(self):
        """Ensure that ordering offers by updated_at returns the expected order of offers in ascending and descending order."""
        url = reverse("offer-list")
        offer_count = Offer.objects.count()
        test_cases = [("updated_at", False), ("-updated_at", True)]
        now = timezone.now()

        Offer.objects.filter(pk=self.offer_web.pk).update(
            created_at=now - timedelta(days=10),
            updated_at=now - timedelta(days=8),
        )
        Offer.objects.filter(pk=self.offer_graphic.pk).update(
            created_at=now - timedelta(days=6),
            updated_at=now - timedelta(days=3),
        )
        Offer.objects.filter(pk=self.offer_social.pk).update(
            created_at=now - timedelta(days=2),
            updated_at=now,
        )

        for param, reverse_flag in test_cases:
            with self.subTest(param=param):
                response = self.client.get(url, {"ordering": param, "page_size": offer_count})

                self.assertEqual(response.status_code, status.HTTP_200_OK)

                updated_at = []
                for offer in response.data["results"]:
                    updated_at.append(offer["updated_at"])

                direction = "descending" if reverse_flag else "ascending"
                error_msg = f"The offers should be sorted {direction}"

                self.assertEqual(len(updated_at), offer_count, msg="The API did not return all the listings.")
                self.assertEqual(updated_at, sorted(updated_at, reverse=reverse_flag), msg=error_msg)


class OfferListPaginationTests(BaseSetupTestCase):
    """
    Tests for pagination of the list of offers, ensuring that the API returns the requested page size and provides
    correct pagination links for next and previous pages.
    """

    def test_list_offers_pagination_returns_requested_page_size_and_navigation_links(self):
        """Ensure that the API returns the requested page size and provides correct pagination links for next and previous pages."""
        url = reverse("offer-list")

        first_page_response = self.client.get(url, {"page_size": 1})

        self.assertEqual(first_page_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(first_page_response.data["results"]), 1)
        self.assertIsNotNone(first_page_response.data["next"])
        self.assertIsNone(first_page_response.data["previous"])

        second_page_response = self.client.get(first_page_response.data["next"])

        self.assertEqual(second_page_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(second_page_response.data["results"]), 1)
        self.assertIsNotNone(second_page_response.data["next"])
        self.assertIsNotNone(second_page_response.data["previous"])
        self.assertNotEqual(first_page_response.data["results"][0]["id"], second_page_response.data["results"][0]["id"])
