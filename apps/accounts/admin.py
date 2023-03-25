from __future__ import annotations

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.http import HttpResponse
from import_export.resources import modelresource_factory, ModelResource

from .models import Account
from .models import UserProfile
from .models import PurchasedCourse
from .resources import PurchasedCourseResource


class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'phone_number', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'phone_number', 'email')


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'image', 'gender', 'birth_date',)
    list_filter = ('user', 'gender',)
    search_fields = ('user',)


admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)


def export_selected_purchased_courses(modeladmin, request, queryset):
    resource = PurchasedCourseResource()
    dataset = resource.export(queryset)
    response = HttpResponse(dataset.xlsx,
                            content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="purchased_courses.xlsx"'
    return response


export_selected_purchased_courses.short_description = 'Export Purchased Course to Excel'


@admin.register(PurchasedCourse)
class PurchasedCourseAdmin(ModelAdmin):
    actions = [export_selected_purchased_courses]
    list_display = ('id', 'user_id', 'user', 'course',)
    list_filter = ('user_id', 'course',)
    exclude = ('created_at', 'updated_at')
    search_fields = ('user_id', 'course',)
