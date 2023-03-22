from rest_framework import serializers
from apps.payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'user', 'course', 'amount', 'payment_type', 'payment_type', 'created_at')


    def validate(self, attrs):
        course_price = attrs['course'].price
        amount = attrs['amount']
        user_id = attrs['user'].id
        if course_price < amount:
            raise serializers.ValidationError('The entered amount is greater than the course amount')
        if course_price > amount:
            raise serializers.ValidationError('The entered amount is less than the course amount')
        # if Payment.objects.filter(user_id=user_id, course_id=attrs['course'].id).exists():
        #     raise serializers.ValidationError('If you have previously purchased this course')

        return attrs