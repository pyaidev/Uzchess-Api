from rest_framework.exceptions import ValidationError
from rest_framework.fields import HiddenField, CurrentUserDefault
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer
from datetime import date
from apps.accounts.api.v1.serializers import AccountSerializer
from apps.accounts.models import Account
from apps.library.models import Book, Category, Wishlist, Order, PromoCode, CheckOut


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


class CreateOrderModelSerializer(ModelSerializer):
    promo_code = PrimaryKeyRelatedField(
        queryset=PromoCode.objects.all(),
        allow_null=True,
        required=False
    )
    user = HiddenField(default=CurrentUserDefault())

    def validate(self, data):
        if data['promo_code'] and data['promo_code'].expiry_date <= date.today():
            raise ValidationError('The promo code has been expired')
        return data

    class Meta:
        model = Order
        fields = (
            'id', 'book', 'quantity', 'promo_code',
            'get_total', 'get_discounted_total', 'user'
        )
        read_only_fields = ('id', 'user')


class BookModelSerializer(ModelSerializer):
    author = AuthorModelSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'author')


class OrderModelSerializer(ModelSerializer):
    book = BookModelSerializer(read_only=True)

    class Meta:
        model = Order
        fields = (
            'id', 'book', 'quantity', 'promo_code',
            'get_total', 'get_discounted_total'
        )


class CreateCheckOutModelSerializer(ModelSerializer):
    class Meta:
        model = CheckOut
        fields = ('id', 'order', 'full_name', 'phone_number', 'email',)


class RetrieveCheckOutModelSerializer(ModelSerializer):
    order = OrderModelSerializer(read_only=True)

    class Meta:
        model = CheckOut
        fields = ('id', 'order', 'order_number')
