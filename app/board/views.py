from rest_framework import generics, authentication, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from django.views.decorators.http import require_http_methods
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import json
from core.models import Board, Pin, User
import pdb
from board import serializers

class BoardViewSet(viewsets.ModelViewSet):
    """Manage Board in the database"""
    serializer_class = serializers.BoardSerializer
    queryset = Board.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # def _params_to_ints(self, qs):
    #     """Convert a list of string IDs to a list of integers"""
    #     return [int(str_id) for str_id in qs.(',')]

    def get_queryset(self):
        """Retrieve the pin for the authenticated user"""
        pin = self.request.query_params.get('pin')
        queryset = self.queryset

        if pin:
            queryset = queryset.filter(pin__id__in=pin_ids)

        return queryset.filter()

    # def pinSelect(request):
    #     if request.method == "PATCH":
    #         board = Board.objects.get(id=self.request.user.id)
    #         print(board)
        # if select_form.is_valid():
        #     print('sucess')
        # else:
        #     print('Fail')

    def get_serializer_class(self):
        return serializers.BoardDetailSerializer

    def perform_create(self, serializer):
        """Create a new board"""
        serializer.save(user=self.request.user)


class BoardPinViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        return serializers.BoardDetailSerializer

    @action(methods=['POST'], detail=True, url_path='add')
    def add_pin(self, request, board_pk=None, pk=None):
        print("////////////////////////")
        print(board_pk)
        print(pk)
        body = json.loads(self.request.body)
        board = Board.objects.get(user_id=board_pk)
        pin = Pin.objects.get(id=pk)
        print(pin)

        board.pin.add(pin)

        serializer = self.get_serializer(
            board,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(methods=['DELETE'], detail=True, url_path='remove')
    def remove_pin(self, request, board_pk=None, pk=None):
        body = json.loads(self.request.body)
        board = Board.objects.get(user_id=board_pk)
        pin = Pin.objects.get(id=pk)

        board.pin.remove(pin)

        serializer = self.get_serializer(
            board,
            data=request.data
        )


        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
