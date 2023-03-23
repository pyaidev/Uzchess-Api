from __future__ import annotations

from django.db import models
from django.core.exceptions import ValidationError

from .choosen import PAY_STATUS
from .choosen import PAY_TYPE
from apps.common.models import BaseModel


class Payment(BaseModel):
    user = models.ForeignKey(
        'accounts.Account', on_delete=models.CASCADE, verbose_name='User',
    )
    course = models.ForeignKey(
        'course.Course', on_delete=models.CASCADE, verbose_name='Course',
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Price',
    )
    payment_type = models.CharField(
        max_length=255, choices=PAY_TYPE, verbose_name='Payment Type',
    )
    payment_status = models.CharField(
        max_length=255, choices=PAY_STATUS, verbose_name='Payment Status'

    )

    def clean(self):
        if self.pk:
            object = Payment.objects.get(pk=self.pk)
            if object.payment_status == 'Failed':
                raise ValidationError('You can not edit failed payment')
            if object.course.price < self.amount:
                raise ValidationError('The entered amount is greater than the course amount')
            if object.course.price > self.amount:
                raise ValidationError('The entered amount is less than the course amount')
            if object.course.title == self.course.title:
                raise ValidationError('If you have previously purchased this course')

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return self.user.first_name
