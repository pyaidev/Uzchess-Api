from __future__ import annotations

from django.contrib import admin

from .models import Payment


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'amount', 'payment_status', 'payment_type', 'created_at')
    list_filter = ('user', 'course', 'amount')
    search_fields = ('user', 'course', 'amount')


# Register your models here.

admin.site.register(Payment, PaymentAdmin)
