from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Pin, Tag, Categories

from pin.serializers import PinSerializer, PinDetailSerializer


PIN_URL = reverse('pin:pin-list')


def sample_tag(user, name='Vegan'):
    """Create and return a sample tag"""
    return Tag.objects.create(user=user, name=name)


def sample_categories(user, name='Coffee Shop'):
    """Create and return a sample categories"""
    return Categories.objects.create(user=user, name=name)

def detail_url(pin_id):
    """Return pin detail URL"""
    return reverse('pin:pin-detail', args=[pin_id])

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

    def test_view_pin_detail(self):
        """Test viewing a pin detail"""
        pin = sample_pin(user=self.user)
        pin.tags.add(sample_tag(user=self.user))
        pin.categories.add(sample_categories(user=self.user))

        url = detail_url(pin.id)
        res = self.client.get(url)

        serializer = PinDetailSerializer(pin)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_pin(self):
        """Test creating pin"""
        payload = {
            'business': 'Storville Coffee',
            'city': 'Seattle',
            'state': 'WA',
            'details': 'Best Coffee in Seattle'
        }
        res = self.client.post(PIN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        pin = Pin.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(pin, key))

    def test_create_pin_with_tags(self):
        """Test creating a pin with tags"""
        tag1 = sample_tag(user=self.user, name='Tag 1')
        tag2 = sample_tag(user=self.user, name='Tag 2')
        payload = {
            'business': 'Storville Coffee',
            'city': 'Seattle',
            'state': 'WA',
            'details': 'Best Coffee in Seattle',
            'title': 'Test recipe with two tags',
            'tags': [tag1.id, tag2.id]
        }
        res = self.client.post(PIN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        pin = Pin.objects.get(id=res.data['id'])
        tags = pin.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_create_pin_with_categories(self):
        """Test creating pin with categories"""
        categories1 = sample_categories(user=self.user, name='Categories 1')
        categories2 = sample_categories(user=self.user, name='Categories 2')
        payload = {
            'business': 'Storville Coffee',
            'city': 'Seattle',
            'state': 'WA',
            'details': 'Best Coffee in Seattle',
            'title': 'Test recipe with two tags',
            'categories': [categories1.id, categories2.id]
        }

        res = self.client.post(PIN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        pin = Pin.objects.get(id=res.data['id'])
        categories = pin.categories.all()
        self.assertEqual(categories.count(), 2)
        self.assertIn(categories1, categories)
        self.assertIn(categories2, categories)

    def test_partial_update_pin(self):
        """Test updating a pin_id with patch"""
        pin = sample_pin(user=self.user)
        pin.tags.add(sample_tag(user=self.user))
        new_tag = sample_tag(user=self.user, name='Curry')

        payload = {'business': 'Bobs Burgers', 'tags': [new_tag.id]}
        url = detail_url(pin.id)
        self.client.patch(url, payload)

        pin.refresh_from_db()
        self.assertEqual(pin.business, payload['business'])
        tags = pin.tags.all()
        self.assertEqual(len(tags), 1)
        self.assertIn(new_tag, tags)

    def test_full_update_pin(self):
        """Test updating a pin with put"""
        pin = sample_pin(user=self.user)
        pin.tags.add(sample_tag(user=self.user))

        payload = {
		    'business': 'Bobs burgers',
            'city': 'Oakland',
            'state': 'CA',
            'details': 'Special of the Day is great',
    		}
        url = detail_url(pin.id)
        self.client.put(url, payload)

        pin.refresh_from_db()
        self.assertEqual(pin.business, payload['business'])
        self.assertEqual(pin.city, payload['city'])
        self.assertEqual(pin.state, payload['state'])
        self.assertEqual(pin.details, payload['details'])
        tags = pin.tags.all()
        self.assertEqual(len(tags), 0)
