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


class Wishlist(models.Model):
    user = ForeignKey('accounts.Account', on_delete=models.CASCADE)
    book = models.ForeignKey('library.Book', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.phone_number}:{self.book.title}'

    class Meta:
        verbose_name = 'Wishlist'
        verbose_name_plural = 'Wishlist'
