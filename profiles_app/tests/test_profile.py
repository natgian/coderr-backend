from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

User = get_user_model()


class ProfileDetailTests(APITestCase):
    """"""

    def test_detail_profile_200_success(self):
        """"""
        url = reverse("profile-detail", kwargs={"pk": 1})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
