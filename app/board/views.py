from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import json
from core.models import Board, Pin, User

from board import serializers

class BoardViewSet(viewsets.ModelViewSet):
    """Manage Board in the database"""
    serializer_class = serializers.BoardSerializer
    queryset = Board.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # def _params_to_ints(self, qs):
    #     """Convert a list of string IDs to a list of integers"""
    #     return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve the pin for the authenticated user"""
        pin = self.request.query_params
        # pin_ids = self._params_to_ints(pin)
        # body = json.loads(self.request.body)
        # pin_id = body['pin']['id']
        # board = Board.objects.get(user=self.request.user.id)
        # print(board, 'im the board')
        # board.save()
        # board.pin.add(pin_id)
        queryset = self.queryset

        # if pin:
        #     queryset = queryset.filter(pin__id__in=pin_ids)

        return queryset.filter()

    def get_serializer_class(self):
        return serializers.BoardDetailSerializer

    def perform_create(self, serializer):
        """Create a new board"""
        serializer.save(user=self.request.user)
        #add this when you have a user attact to the board
        # serializer.save(user=self.request.user)

    # @action(methods=['PATCH'], detail=True, url_path='board/board/1'))
    # def patch(self, serializer):
    #     """Add a Pin to Board"""
    #     board = Board.objects.get(user=self.request.user)
    #     board.pin.add(pin)
    #     board.save()
