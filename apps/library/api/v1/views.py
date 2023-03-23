from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView, CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.library.api.v1.serializers import ListBookModelSerializer, RetrieveBookModelSerializer, \
    CreateWishlistModelSerializer
from apps.library.models import Book, Wishlist


class ListBookAPIView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = ListBookModelSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('id', 'title', 'about', 'category__title')
    filterset_fields = ('language', 'level', 'category__title', 'rate')
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)


class RetrieveBookAPIView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = RetrieveBookModelSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = 'slug'


class CreateWishlistAPIView(CreateAPIView):
    serializer_class = CreateWishlistModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Wishlist.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
