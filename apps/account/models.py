from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework_simplejwt.tokens import RefreshToken

from apps.common.models import BaseModel

from .choosen import GENDER
from ..course.models import Course


class AccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, phone_number, password=None, **extra_fields):
        user = self.model(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, phone_number, password=None, **extra_fields):
        user = self.model(phone_number=phone_number, first_name=first_name,
                          last_name=last_name, password=make_password(password))
        user.is_superuser = True
        user.is_staff = True
        user.is_sponsor = True
        user.is_active = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin, BaseModel):
    """ Account model """
    first_name = models.CharField(
        max_length=50, blank=True,
        null=True, verbose_name='Name',
    )
    last_name = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='Surname',
    )
    username = models.CharField(
        max_length=255, blank=True, null=True, unique=True, verbose_name='Phone',
    )
    phone_number = PhoneNumberField(region='UZ', unique=True, verbose_name='Phone number')
    email = models.EmailField(
        max_length=255, blank=True, null=True, verbose_name='Email',
    )
    email_is_verified = models.BooleanField(
        default=False, verbose_name='Email is verified',
    )
    is_superuser = models.BooleanField(default=False, verbose_name='Superuser')
    is_staff = models.BooleanField(default=False, verbose_name='Admin')
    is_active = models.BooleanField(default=True)
    date_login = models.DateTimeField(auto_now=True, verbose_name='Date login')
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name='Date created',
    )

    objects = AccountManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.first_name

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return data


class UserProfile(BaseModel):
    """ User profile model """
    user = models.OneToOneField(
        Account, on_delete=models.CASCADE, related_name='profile', verbose_name='User',
    )
    bio = models.TextField(max_length=500, blank=True, verbose_name='Bio')
    image = models.ImageField(
        upload_to='profile/',
        null=True, blank=True, verbose_name='Image',
    )
    gender = models.CharField(
        max_length=211, choices=GENDER, blank=True, verbose_name='Gender',
    )
    birth_date = models.DateField(
        null=True, blank=True, verbose_name='Birth date'
    )

    class Meta:
        verbose_name = 'User profile'
        verbose_name_plural = 'User profiles'

    def __str__(self):
        return self.user.first_name


class PurchasedCourse(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey('account.Account', on_delete=models.CASCADE)
    lessons_video_count = models.PositiveIntegerField(default=0)
    viewed_video_count = models.PositiveIntegerField(default=0)
    is_finished = models.BooleanField(default=True)
    def __str__(self):
        return self.course.title



    class Meta:
        verbose_name = 'Purchase Course'
        verbose_name_plural = 'Purchase Courses'