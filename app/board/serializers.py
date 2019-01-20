from rest_framework import serializers, request
from pin.serializers import PinSerializer, TagSerializer, CategoriesSerializer
from user.serializers import UserSerializer

# added this to see if we can get details
from core.models import Board, Pin

class BoardSerializer(serializers.ModelSerializer):
    """Serializer for user board pins"""
    pin = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Pin.objects.all()
    )

    class Meta:
        model = Board
        fields = ( 'pin', 'user',)

class BoardDetailSerializer(BoardSerializer, PinSerializer):
    pin = PinSerializer(many=True, read_only=True)
    # user = UserSerializer(read_only=True)
