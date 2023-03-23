from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.library.models import Category, Book, Wishlist, PromoCode, Order, CheckOut


@admin.register(Category)
class CategoryModelAdmin(ModelAdmin):
    list_display = ('id', 'title')
    list_filter = ('id', 'title')
    fields = ('title',)
    exclude = ('slug',)
    search_fields = ('title',)


@admin.register(Book)
class BookModelAdmin(ModelAdmin):
    list_display = ('id', 'title', 'author_first_name',
                    'category_title', 'get_discount', 'get_avg_rate', 'year'
                    )
    list_filter = ('id', 'category', 'level', 'rate', 'language', 'category')
    fields = ('title', 'author',
              'image', 'category', 'number_of_pages',
              'price', 'rate', 'language', 'level',
              'discount', 'about'
              )
    exclude = ('slug', 'year')
    search_fields = ('id', 'title')
    ordering = ('id',)

    def author_first_name(self, obj):
        return obj.author.first_name

    author_first_name.short_description = 'Author'

    def category_title(self, obj):
        return obj.category.title

    category_title.admin_order_field = 'category__title'
    category_title.short_description = 'Category'


@admin.register(Wishlist)
class WishlistModelAdmin(ModelAdmin):
    fields = ('book', 'user')
    ordering = ('id',)


@admin.register(PromoCode)
class PromoCodeAdmin(ModelAdmin):
    fields = ('code', 'discount', 'expiry_date')
    list_display = ('code', 'discount', 'expiry_date')


@admin.register(Order)
class OrderModelAdmin(ModelAdmin):
    fields = ('book', 'quantity', 'user', 'promo_code')
    list_display = ('book_title', 'quantity', 'user_first_name', 'get_total', 'get_discounted_total')
    ordering = ('id',)

    def book_title(self, obj):
        return obj.book.title

    book_title.admin_order_field = 'book__title'

    def user_first_name(self, obj):
        return obj.user.first_name

    user_first_name.short_description = 'User'


@admin.register(CheckOut)
class CheckOutModelAdmin(ModelAdmin):
    fields = ('order', 'full_name', 'phone_number', 'email', 'status')
    list_display = ('id', 'order', 'full_name', 'phone_number', 'status', 'order_number')
    ordering = ('id',)
