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

        # pin_id = self.request.query_params
        # print(pin_id)
        # # pin_ids = self._params_to_ints(pin)
        # body = json.loads(self.request.body)
        # print(body)
        # # pin_id = body['pin']['id']
        # board = Board.objects.get(user=self.request.user.id)
        # print(board, 'im the board')
        # # board.save()
        # board.pin.add(pin_id)
        queryset = self.queryset

        # if pin:
        #     queryset = queryset.filter(pin__id__in=pin_ids)

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
        #add this when you have a user attact to the board
        # serializer.save(user=self.request.user)


class BoardPinViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        return serializers.BoardDetailSerializer

    @action(methods=['POST'], detail=True, url_path='add')
    def add_pin(self, request, board_pk=None, pk=None):
        body = json.loads(self.request.body)
        board = Board.objects.get(user_id=board_pk)
        pin = Pin.objects.get(id=pk)
        print(pin)

        board.pin.add(pin)

        # pin = request.POST
        # print(pin,"im the request")
        serializer = self.get_serializer(
            board,
            data=request.data
        )

        # pdb.set_trace();
        # board.save()

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


    #     serializer_class = serializers.BoardSerializer
    #
    #     print('yo')
    #     board = Board.objects.get(user=4)
    #     return Response(board,status=status.HTTP_200_OK)
    # @action(methods=['GET'], detail=True, url_path='1/')
    # def pin_to_board(self, request):
    #     """Add a Pin to Board"""
    #     print("blah")
    #     # board = Board.objects.get(id=id)
    #     # print(board)
    #     return '["yay!"]'
        # board.pin.add(pin)
        # board.save()

# class ManageBoardView(generics.RetrieveUpdateAPIView):
#     """Manage the authenticated user"""
#     serializer_class = BoardSerializer
#     authentication_classes = (authentication.TokenAuthentication,)
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def get_object(self):
#         return self.request.user
