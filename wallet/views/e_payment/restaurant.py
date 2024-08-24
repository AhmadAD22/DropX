from rest_framework.views import APIView
from accounts.models import RestaurantSubscription
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from utils.payment.payment_subscription import RestaurantSubscriptionPayment



class RestaurantPaysubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            subscription = RestaurantSubscription.objects.get(restaurant__phone=request.user.phone)
        except RestaurantSubscription.DoesNotExist:
            return Response({'erorr':'The subscription does not found!'},status=status.HTTP_404_NOT_FOUND)
        payment_respons=RestaurantSubscriptionPayment.initiate_payment(subscription=subscription,request=request)
        if payment_respons.status_code == 200:
            return Response(payment_respons.json())
        
        else: 
            
            return Response({'error': payment_respons.text})