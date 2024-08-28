from rest_framework import serializers
from order.models import Coupon

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'type', 'restaurant', 'driver', 'code', 'percent', 'expireAt', 'times', 'isActive']