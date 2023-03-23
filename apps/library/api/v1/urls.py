from django.urls import path

from apps.library.api.v1.views import ListBookAPIView, RetrieveBookAPIView, CreateWishlistAPIView, CreateOrderAPIView, \
    CreateCheckOutAPIView, RetrieveCheckOutAPIVIew

urlpatterns = [
    path('list/books/', ListBookAPIView.as_view(), name='list_book'),
    path('list/retrieve/<str:slug>/', RetrieveBookAPIView.as_view(), name='retrieve_book'),
    path('create/wishlist/', CreateWishlistAPIView.as_view(), name='wishlist_create'),
    path('create/order/', CreateOrderAPIView.as_view(), name='order_create'),
    path('create/checkout/', CreateCheckOutAPIView.as_view(), name='checkout_create'),
    path('retrieve/checkout/<int:order_number>/', RetrieveCheckOutAPIVIew.as_view(), name='checkout_retrieve')
]

