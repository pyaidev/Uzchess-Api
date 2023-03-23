from __future__ import annotations

from django.contrib import admin

from .models import Account
from .models import UserProfile
from .models import PurchasedCourse


class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'phone_number', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'phone_number', 'email')



class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'image', 'gender', 'birth_date', )
    list_filter = ('user', 'gender', )
    search_fields = ('user', )


class PurchasedCourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'user', 'course', )
    list_filter = ('user_id', 'course', )
    search_fields = ('user_id', 'course',)


admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(PurchasedCourse, PurchasedCourseAdmin)