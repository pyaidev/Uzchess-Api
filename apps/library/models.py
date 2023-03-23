from datetime import date
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CharField, SlugField, ForeignKey, CASCADE, IntegerField, DecimalField, TextField, \
    DateField, FloatField, ImageField, Avg, ManyToManyField, SET_NULL, EmailField
from phonenumber_field.modelfields import PhoneNumberField
import random
# from apps.account.models import Account
from apps.common.models import BaseModel
from apps.library.choices import LanguageChoices, LevelChoices, StatusChoices
import uuid


class Category(BaseModel):
    title = CharField(max_length=255)
    slug = SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Category Model'


class Book(BaseModel):
    title = CharField(max_length=255)
    slug = SlugField(max_length=255, unique=True)
    author = ForeignKey('accounts.Account', limit_choices_to={'is_author': True}, on_delete=CASCADE)
    image = ImageField(upload_to='books/%Y/%m/%d')
    category = ForeignKey('library.Category', CASCADE)
    number_of_pages = IntegerField(default=0)
    price = DecimalField(max_digits=6, decimal_places=2)
    rate = FloatField(validators=[
        MaxValueValidator(5.0, 'The rate cannot be high than 5.0'),
        MinValueValidator(1.0, 'The rate cannot be less than 1.0')
    ])
    language = CharField(max_length=25, choices=LanguageChoices.choices, default=LanguageChoices.UZB)
    level = CharField(max_length=25, choices=LevelChoices.choices, default=LevelChoices.BEGINNER)
    discount = IntegerField(default=0)
    about = TextField()
    year = DateField(auto_now_add=True)

    @property
    def get_discount(self):
        return int(self.price) - (int(self.price) * (self.discount / 100))

    @property
    def get_avg_rate(self):
        rate = Book.objects.aggregate(avg_rate=Avg('rate'))['avg_rate']
        return rate

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Book'


class PromoCode(BaseModel):
    code = CharField(max_length=50)
    discount = FloatField(default=0)
    expiry_date = DateField()

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'PromoCode'
        verbose_name_plural = 'PromoCode'


class Wishlist(BaseModel):
    user = ForeignKey('accounts.Account', on_delete=models.CASCADE)
    book = models.ForeignKey('library.Book', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.phone_number}:{self.book.title}'

    class Meta:
        verbose_name = 'Wishlist'
        verbose_name_plural = 'Wishlist'


class Order(BaseModel):
    book = ForeignKey('library.Book', CASCADE)
    quantity = IntegerField(default=1)
    user = ForeignKey('accounts.Account', CASCADE, limit_choices_to={
        'is_author': False
    })
    promo_code = ForeignKey('library.PromoCode', SET_NULL, null=True, blank=True)

    def validate(self):
        if self.promo_code.expiry_date <= date.today():
            raise ValidationError({'message': 'The code has been expired'})

    @property
    def get_total(self):
        if self.book.discount:
            total = self.quantity * self.book.get_discount
        else:
            total = self.quantity * self.book.price
        return total

    @property
    def get_discounted_total(self):
        if self.promo_code:
            return self.get_total - self.promo_code.discount
        else:
            return self.get_total

    def __str__(self):
        return f'{self.book.title}:{self.user.phone_number}'

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Order'


class CheckOut(BaseModel):
    order = ForeignKey('library.Order', CASCADE)
    full_name = CharField(max_length=255)
    phone_number = PhoneNumberField(region='UZ')
    email = EmailField()
    status = CharField(max_length=50, choices=StatusChoices.choices, default=StatusChoices.NEW)
    order_number = IntegerField(default=random.randint(1, 999999999))

    def __str__(self):
        return f'{self.full_name}:{self.order_number}'

    class Meta:
        verbose_name = 'CheckOut'
        verbose_name_plural = 'CheckOut'
