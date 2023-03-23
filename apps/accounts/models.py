from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.db import models
from django.db.models import Sum
from django.db.models.signals import pre_save
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework_simplejwt.tokens import RefreshToken

from apps.common.models import BaseModel

from .choosen import GENDER
from ..course.models import Course, CourseLesson


class AccountManager(BaseUserManager):
    def create_user(self, first_name, email, password=None, **extra_fields):
        user = self.model(
            first_name=first_name,
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


AUTH_PROVIDERS = {'google': 'google', 'email': 'email'}


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
    phone_number = PhoneNumberField(region='UZ', verbose_name='Phone number', unique=True)
    email = models.EmailField(
        max_length=255, blank=True, null=True, unique=True, verbose_name='Email',
    )
    email_is_verified = models.BooleanField(
        default=False, verbose_name='Email is verified',
    )
    is_superuser = models.BooleanField(default=False, verbose_name='Superuser')
    is_staff = models.BooleanField(default=False, verbose_name='Admin')
    is_active = models.BooleanField(default=True)
    is_author = models.BooleanField(default=False)
    date_login = models.DateTimeField(auto_now=True, verbose_name='Date login')
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name='Date created',
    )
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))

    objects = AccountManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

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

    @property
    def get_wishlist(self):
        wishlist = self.wishlist_set.filter(user=self).values()
        return list(wishlist)


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
    user = models.ForeignKey('accounts.Account', on_delete=models.CASCADE)
    lessons_video_count = models.PositiveIntegerField(default=0)
    viewed_video_count = models.PositiveIntegerField(default=0)
    is_finished = models.BooleanField(default=True)
    def __str__(self):
        return self.course.title

    class Meta:
        verbose_name = 'Purchase Course'
        verbose_name_plural = 'Purchase Courses'


def purchase_course_post_save(instance, sender, *args, **kwargs):
    if instance is not None:
        obj = CourseLesson.objects.filter(course__id=instance.course.id).aggregate(Sum('video_count'))
        instance.lessons_video_count = obj.get('video_count__sum')


pre_save.connect(purchase_course_post_save, sender=PurchasedCourse)
