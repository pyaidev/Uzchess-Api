from rest_framework.serializers import ModelSerializer

from apps.account.api.v1.serializers import AccountSerializer
from apps.account.models import Account
from apps.library.models import Book, Category, Wishlist


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title')


class AuthorModelSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'first_name', 'last_name')


class ListBookModelSerializer(ModelSerializer):
    author = AuthorModelSerializer(read_only=True)
    category = CategoryModelSerializer(read_only=True)

    class Meta:
        model = Book
        fields = (
            'id', 'title', 'price', 'slug',
            'get_discount', 'level', 'category',
            'author', 'language', 'image', 'get_avg_rate',
        )


class RetrieveBookModelSerializer(ModelSerializer):
    author = AuthorModelSerializer(read_only=True)

    class Meta:
        model = Book
        fields = (
            'id', 'title', 'price',
            'get_discount', 'level',
            'number_of_pages', 'author',
            'image', 'year', 'about'
        )


class CreateWishlistModelSerializer(ModelSerializer):
    class Meta:
        model = Wishlist
        fields = (
            'id', 'user', 'book'
        )
