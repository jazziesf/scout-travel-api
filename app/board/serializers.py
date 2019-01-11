from rest_framework import serializers

from core.models import Board, Pin

class BoardSerializer(serializers.ModelSerializer):
    """Serializer for user board pins"""
    pin = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Pin.objects.all()
    )

    class Meta:
        model = Board
        fields = ('pin', 'user',)
        # read_only_fields = ('id',)
