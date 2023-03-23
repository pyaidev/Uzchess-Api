from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView, CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.library.api.v1.serializers import ListBookModelSerializer, RetrieveBookModelSerializer, \
    CreateWishlistModelSerializer, CreateOrderModelSerializer, CreateCheckOutModelSerializer, \
    RetrieveCheckOutModelSerializer
from apps.library.models import Book, Wishlist, Order, CheckOut


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


class CreateOrderAPIView(CreateAPIView):
    serializer_class = CreateOrderModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CreateCheckOutAPIView(CreateAPIView):
    queryset = CheckOut.objects.all()
    serializer_class = CreateCheckOutModelSerializer
    permission_classes = (IsAuthenticated,)


class RetrieveCheckOutAPIVIew(RetrieveAPIView):
    queryset = CheckOut.objects.all()
    serializer_class = RetrieveCheckOutModelSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'order_number'
