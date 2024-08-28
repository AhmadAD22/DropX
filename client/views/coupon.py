from rest_framework.views import APIView
from rest_framework.response import Response
from order.models import Coupon
from ..serializers.coupon import CouponSerializer

class CouponListAPIView(APIView):
    def get(self, request):
        coupons = Coupon.objects.all()
        grouped_coupons = {
            'expired': [],
            'active': []
        }

        for coupon in coupons:
            if coupon.is_expired():
                grouped_coupons['expired'].append(CouponSerializer(coupon).data)
            else:
                grouped_coupons['active'].append(CouponSerializer(coupon).data)

        return Response(grouped_coupons)