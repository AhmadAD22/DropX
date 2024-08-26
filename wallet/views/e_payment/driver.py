from rest_framework.views import APIView
from accounts.models import DriverOrderSubscription,DriverTripSubscription
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from utils.payment.payment_subscription import PaymentDriverOrderSubscription,PaymentDriverTripSubscription
from ...models import DriverOrderSubscriptionPayment,DriverTripSubscriptionPayment



class DriverOrderPaysubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            subscription = DriverOrderSubscription.objects.get(driver__phone=request.user.phone)
        except DriverOrderSubscription.DoesNotExist:
            return Response({'erorr':'The subscription does not found!'},status=status.HTTP_404_NOT_FOUND)
        subscription_req=DriverOrderSubscriptionPayment.objects.filter(subscription=subscription,paid=False)
        payment_respons=PaymentDriverOrderSubscription.initiate_payment(subscription_req=subscription_req.first(),request=request)
        if payment_respons.status_code == 200:
            return Response(payment_respons.json())
        
        else: 
            
            return Response({'error': payment_respons.text})
        
        
class DriverTripPaysubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            subscription = DriverTripSubscription.objects.get(driver__phone=request.user.phone)
        except DriverTripSubscription.DoesNotExist:
            return Response({'erorr':'The subscription does not found!'},status=status.HTTP_404_NOT_FOUND)
        subscription_req=DriverTripSubscriptionPayment.objects.filter(subscription=subscription,paid=False)
        payment_respons=PaymentDriverTripSubscription.initiate_payment(subscription_req=subscription_req.first(),request=request)
        if payment_respons.status_code == 200:
            return Response(payment_respons.json())
        
        else: 
            
            return Response({'error': payment_respons.text})