from rest_framework import serializers, request
from pin.serializers import PinSerializer
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

    # def update(self, instance, validated_data):
    #     """Update a user, setting the password correctly and return it"""
    #     pin = (self)
    #     print(pin)
    #     board = super().update()
    #     print(board.user.id)
    #
    #     board.pin.add(Pin.objects.get(self.request))
    #     board.save
    #
    #     return board


class BoardDetailSerializer(BoardSerializer):
    pin = PinSerializer(many=True, read_only=True)
    # user = UserSerializer(read_only=True)
