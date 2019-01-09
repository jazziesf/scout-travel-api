from rest_framework import serializers

from core.models import Tag, Categories, Pin


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


class PinSerializer(serializers.ModelSerializer):
    """Serialize a pin"""
    categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Categories.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Pin
        fields = (
            'id', 'business', 'city', 'tags', 'state', 'details',
            'categories',
        )
        read_only_fields = ('id',)


class PinDetailSerializer(PinSerializer):
    categories = CategoriesSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
