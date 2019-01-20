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

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        assigned_only = bool(self.request.query_params.get('assigned_only'))
        queryset = self.queryset

        if assigned_only:
            queryset = queryset.filter(pin__isnull=False)
            print(queryset)

        return queryset.filter(user=self.request.user).order_by('-name')

    # def _params_to_ints(self, qs):
    #     """Convert a list of string IDs to a list of integers"""
    #     return [int(str_id) for str_id in qs.(',')]

    def get_queryset(self):
        """Retrieve the pin for the authenticated user"""
        pin = self.request.query_params.get('pin')
        queryset = self.queryset
        # print("//////////////////// THIS COMBO WORKS DONT MOVE IT //////")
        # board = Board.objects.get(user=self.request.user)
        # # print(board, "::::::::::  this return bob or the user :::::::")
        # #
        # pin = Pin.objects.filter(board=board) #this is a test the rest works between the ////
        # print(pin)
        # print(pin, "///////  this return the pins on the user board //////")
        # # pin = Pin.objects.all(board=board) this does not work
        #
        # queryset = self.queryset.filter(user=board)
        # # this works returns bob for board
        # # queryset = self.queryset
        # print(queryset, "???????  this return bob board ??????")
        if pin:
            queryset = queryset.filter(pin=pin)
        #     queryset = queryset.filter(pin=pin)
        #
        #     print(queryset, "im the pin query set")


        return queryset


    def get_serializer_class(self):
        return serializers.BoardDetailSerializer

    def perform_create(self, serializer):
        """Create a new board"""
        serializer.save(user=self.request.user)


class BoardPinViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PinSerializer
    queryset = Pin.objects.all()
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)


    def get_serializer_class(self):
        return serializers.BoardDetailSerializer

    def get_queryset(self):
        """Retrieve the pin for the authenticated user"""
        queryset = self.queryset
        # print(pin)
        # city = self.request.query_params.get('city')
        pin = self.request.query_params.get('pin')
        print(pin, "pinviewset")
        # queryset = queryset.filter(pin__isnull=False)
        # print("//////////////////// THIS COMBO WORKS DONT MOVE IT //////")
        # board = Board.objects.get(user=self.request.user)
        # print(board, "::::::::::  this return bob or the user :::::::")
        # #
        # pin = Pin.objects.all(board=board) #this is a test the rest works between the ////
        # print(queryset, "///////  this return the pins on the user board //////")
        # # pin = Pin.objects.all(board=board) this does not work
        # board = Board.objects.filter(pin__city='pin__city')
        # pin = Board.objects.filter(pin__city="pin_city").prefetch_related('pin')
        # print(pin)
        # queryset = self.queryset
        # # this works returns bob for board
        # # queryset = self.queryset
        # print(queryset, "???????  this return bob board ??????")
        #

        if pin:
            queryset = queryset.filter(id=id)
            # queryset = queryset.filter(pin=pin)
        #
        #     print(queryset, "im the pin query set in boardview")


        return queryset

        print('//////////////')

    @action(methods=['POST'], detail=True, url_path='add')
    def add_pin(self, request, board_pk=None, pk=None):
        body = json.loads(self.request.body)
        board = Board.objects.get(user_id=board_pk)
        pin = Pin.objects.get(id=pk)

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

    # @action(methods=['GET'], detail=True, url_path='details')
    # def detail_pin(self, request, board_pk=None, pk=None):
    #     # body = json.loads(self.request.body)
    #     board = Board.objects.get(user_id=board_pk)
    #     print(board)
    #     pin = Pin.objects.get(id=pk)
    #     print(pin)
    #
    #
    #     serializer = self.get_serializer(
    #         pin,
    #         data=request.data
    #     )
    #
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(
    #             serializer.data,
    #             status=status.HTTP_200_OK
    #         )
    #
    #     return Response(
    #         serializer.errors,
    #         status=status.HTTP_400_BAD_REQUEST
    #     )
