from rest_framework import serializers

from core.models import Tag, Categories


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag object"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_Fields = ('id',)

class CategoriesSerializer(serializers.ModelSerializer):
    """Serializer for an categories object"""

    class Meta:
        model = Categories
        fields = ('id', 'name')
        read_only_fields = ('id',)
