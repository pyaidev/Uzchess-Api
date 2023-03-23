from django.urls import path

from apps.library.api.v1.views import ListBookAPIView, RetrieveBookAPIView, CreateWishlistAPIView

urlpatterns = [
    path('list/books/', ListBookAPIView.as_view(), name='list_book'),
    path('list/retrieve/<str:slug>/', RetrieveBookAPIView.as_view(), name='retrieve_book'),
    path('create/wishlist/', CreateWishlistAPIView.as_view(), name='wishlist_create')

]
