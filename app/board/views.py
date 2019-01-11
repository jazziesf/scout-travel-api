from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Board, Pin

from board import serializers

class BoardViewSet(viewsets.ModelViewSet):
    """Manage Board in the database"""
    serializer_class = serializers.BoardSerializer
    queryset = Board.objects.all()

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve the pin for the authenticated user"""
        pin = Pin.objects.filter(user=self.request.user)
        pin = self.request.query_params.get('pin')
        queryset = self.queryset
        if pin:
            pin_ids = self._params_to_ints(pin)
            queryset = queryset.filter(pin__business__in=pin_ids)
        # # if categories:
        # #     ingredient_ids = self._params_to_ints(categories)
        # #     queryset = queryset.filter(categories__id__in=ingredient_ids)

        return queryset

    def perform_create(self, serializer):
        """Create a new pin"""
        serializer.save(user=self.request.user)
        #add this when you have a user attact to the board
        # serializer.save(user=self.request.user)
