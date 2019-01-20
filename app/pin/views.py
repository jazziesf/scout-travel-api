from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Categories, Pin

from pin import serializers
# from . import requests


class BasePinAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """Base viewset for user owned pin attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        assigned_only = bool(self.request.query_params.get('assigned_only'))
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(pin__isnull=False)

        return queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class TagViewSet(BasePinAttrViewSet):
    """Manage tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class CategoriesViewSet(BasePinAttrViewSet):
    """Manage categories in the database"""
    queryset = Categories.objects.all()
    serializer_class = serializers.CategoriesSerializer


class PinViewSet(viewsets.ModelViewSet):
    """Manage pin in the database"""
    serializer_class = serializers.PinSerializer
    queryset = Pin.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    # ////// move your view for guest users /////////


    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve the pin for the authenticated user"""
        tags = self.request.query_params.get('tags')
        categories = self.request.query_params.get('categories')
        state = self.request.query_params.get('state')
        city = self.request.query_params.get('city')

        queryset = self.queryset

        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if categories:
            ingredient_ids = self._params_to_ints(categories)
            queryset = queryset.filter(categories__id__in=ingredient_ids)
        if state:
            queryset = queryset.filter(state__istartswith=state)
        if city:
            queryset = queryset.filter(city=city) or queryset.filter(city__startswith=city[0])

        return queryset
        # queryset.filter(user=self.request.user) this may query by only users removed it

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.PinDetailSerializer
        elif self.action == 'upload_image':
            return serializers.PinImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new pin"""
        return serializer.save(user=self.request.user)

        # serializer.save(user=self.request.user)
        # this was causing me errors removed it to work in frontend but
        #need to add it back again error expecting User instance

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a pin"""
        pin = self.get_object()
        serializer = self.get_serializer(
            pin,
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
