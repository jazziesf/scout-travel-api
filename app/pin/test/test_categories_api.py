from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Categories, Pin

from pin.serializers import CategoriesSerializer


CATEGORIES_URL = reverse('pin:categories-list')


class PublicIngredientsApiTests(TestCase):
    """Test the publically available ingredients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access this endpoint"""
        res = self.client.get(CATEGORIES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsAPITests(TestCase):
    """Test categories can be retrieved by authorized user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@londonappdev.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_categories_list(self):
        """Test retrieving a list of categories"""
        Categories.objects.create(user=self.user, name='kale')
        Categories.objects.create(user=self.user, name='salt')

        res = self.client.get(CATEGORIES_URL)

        categories = Categories.objects.all().order_by('-name')
        serializer = CategoriesSerializer(categories, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_categories_limited_to_user(self):
        """Test that only categories for authenticated user are returned"""
        user2 = get_user_model().objects.create_user(
            'other@londonappdev.com',
            'testpass'
        )
        Categories.objects.create(user=user2, name='Seattle')

        categories = Categories.objects.create(user=self.user, name='vegan')

        res = self.client.get(CATEGORIES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], categories.name)

    def test_create_categories_successful(self):
        """Test creating a new categories"""
        payload = {'name': 'Coffee'}
        self.client.post(CATEGORIES_URL, payload)

        exists = Categories.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_categories_invalid(self):
        """Test creating invalid ingredient fails"""
        payload = {'name': ''}
        res = self.client.post(CATEGORIES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_categories_assigned_to_pin(self):
        """Test filtering categories by those assigned to pins"""
        categories1 = Categories.objects.create(
            user=self.user, name='Burger'
        )
        categories2 = Categories.objects.create(
            user=self.user, name='Rooftop'
        )
        pin = Pin.objects.create(
            business= 'Bobs burgers',
            city='Oakland',
            state='CA',
            details='Special of the Day is great',
            user=self.user
        )
        pin.categories.add(categories1)

        res = self.client.get(CATEGORIES_URL, {'assigned_only': 1})

        serializer1 = CategoriesSerializer(categories1)
        serializer2 = CategoriesSerializer(categories2)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)
