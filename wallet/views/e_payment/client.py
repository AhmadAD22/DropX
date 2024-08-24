from rest_framework.views import APIView
from order.models import Order,Trip
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from utils.payment.order_pyment import Orderpayment,TripPayment



class ClientPayOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request,order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({'erorr':'The order does not found!'},status=status.HTTP_404_NOT_FOUND)
        payment_respons=Orderpayment.initiate_payment(order=order,request=request)
        print(payment_respons)
        if payment_respons.status_code == 200:
            return Response(payment_respons.json())
        
        else: 
            
            return Response({'error': payment_respons.text})
        
class ClientPayTripAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request,trip_id):
        try:
            trip = Trip.objects.get(id=trip_id)
        except Trip.DoesNotExist:
            return Response({'erorr':'The trip does not found!'},status=status.HTTP_404_NOT_FOUND)
        payment_respons=TripPayment.initiate_payment(trip=trip,request=request)
        print(payment_respons)
        if payment_respons.status_code == 200:
            return Response(payment_respons.json())
        
        else: 
            
            return Response({'error': payment_respons.text})