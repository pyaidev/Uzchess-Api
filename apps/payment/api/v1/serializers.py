from rest_framework import serializers

from apps.accounts.models import PurchasedCourse
from apps.payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'user', 'course', 'amount', 'payment_type', 'payment_status', 'created_at')


    def validate(self, attrs):
        course_price = attrs['course'].price
        amount = attrs['amount']
        payment_status = attrs['payment_status']
        user_id = attrs['user']
        if course_price < amount:
            raise serializers.ValidationError('The entered amount is greater than the course amount')
        if course_price > amount:
            raise serializers.ValidationError('The entered amount is less than the course amount')
        # if Payment.course.name in PurchasedCourse.course.name:
        #     raise serializers.ValidationError('This course is already purchased')

        return attrs