from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Pin

from pin.serializers import PinSerializer


PIN_URL = reverse('pin:pin-list')


def sample_pin(user, **params):
    """Create and return a sample pin"""
    defaults = {
        'business': 'Storville Coffee',
        'city': 'Seattle',
        'state': 'WA',
        'details': 'Best Coffee in Seattle'
    }
    defaults.update(params)

    return Pin.objects.create(user=user, **defaults)


class PublicPinApiTests(TestCase):
    """Test unauthenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()

    def test_required_auth(self):
        """Test the authenticaiton is required"""
        res = self.client.get(PIN_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePinApiTests(TestCase):
    """Test authenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@londonappdev.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_pin(self):
        """Test retrieving list of pin"""
        sample_pin(user=self.user)
        sample_pin(user=self.user)

        res = self.client.get(PIN_URL)

        pin = Pin.objects.all().order_by('-id')
        serializer = PinSerializer(pin, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_pin_limited_to_user(self):
        """Test retrieving pin for user"""
        user2 = get_user_model().objects.create_user(
            'other@londonappdev.com',
            'pass'
        )
        sample_pin(user=user2)
        sample_pin(user=self.user)

        res = self.client.get(PIN_URL)

        pin = Pin.objects.filter(user=self.user)
        serializer = PinSerializer(pin, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)
