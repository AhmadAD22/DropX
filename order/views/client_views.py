from rest_framework.views import APIView
from ..models import *
from ..serializers.client_serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.models import Client,CarCategory
from utils.geographic import calculate_distance
from utils.payment.order_pyment import Orderpayment
from datetime import date
class TripCarAPIView(APIView):
    
    def get(self, request, *args, **kwargs):
        cars = CarCategory.objects.all()
         # Get distance from query parameter
        source_lat = request.query_params.get('source_lat')
        source_lon = request.query_params.get('source_lon')
        destenation_lat = request.query_params.get('destenation_lat')
        destenation_lon = request.query_params.get('destenation_lon')
        distance=calculate_distance(source_lat,source_lon,destenation_lat,destenation_lon)
        serializer = TripCarSerializer(cars, context={'distance': distance},many=True)
        return Response(serializer.data)
    
    


class ClientCreateTripAPIView(APIView):
    def post(self, request):
        try:
            client=Client.objects.get(phone=request.user.phone)
        except Client.DoesNotExist:
            return Response({"error":"client does not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = TripSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(client=client,status=Status.PENDING)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TripDetailAPIView(APIView):
    def get(self, request, trip_id):
        try:
            trip = Trip.objects.get(id=trip_id)
            serializer = TripSerializer(trip)
            return Response(serializer.data)
        except Trip.DoesNotExist:
            return Response({'message': 'Trip not found'}, status=404)
 
 
class ClientCurrentTripsListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        trips = Trip.objects.filter(
            Q(client=request.user) &
            (Q(status='IN_PROGRESS') | Q(status='PENDING')| Q(status=Status.ACCEPTED)) 
                  )
        serializer = TripListSerializer(trips, many=True)
        return Response(serializer.data) 
    
class ClientPreviousTripsListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        trips = Trip.objects.filter(
            Q(client=request.user) &
            (Q(status=Status.COMPLETED) | Q(status=Status.CANCELLED)| Q(status=Status.REJECTED)) 
                  )
        serializer = TripListSerializer(trips, many=True)
        return Response(serializer.data)          
        
class ClientCurrentOrdersListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        orders = Order.objects.filter(
            Q(client=request.user) &
            (Q(status='IN_PROGRESS') | Q(status='PENDING')) 
                  )
        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data)
    
class ClientPreviousOrdersListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        orders = Order.objects.filter(
            Q(client=request.user) &
            (Q(status=Status.COMPLETED) | Q(status=Status.CANCELLED)| Q(status=Status.REJECTED)) 
                  )
        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data)
    
class ClientOrderDetailsListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({'erorr':'The order does not found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = ClientOrderSerializer(order)
        return Response(serializer.data)
    
class ClientCancelOrderListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request,order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({'erorr':'The order does not found!'},status=status.HTTP_404_NOT_FOUND)
        if order.status==Status.PENDING:
            cancelled_order_count=Order.objects.filter(client=request.user,status=Status.CANCELLED,orderDate__date=date.today(),).count()
            orderConfig=OrderConfig.objects.first()
            if cancelled_order_count <= orderConfig.maxRejectedNumber:
                order.status=Status.CANCELLED
                order.save()
                serializer = ClientOrderSerializer(order)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response({'erorr':'Exceeded cancellation limit!'},status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response({'erorr':'Only pending orders can be cancelled!'},status=status.HTTP_400_BAD_REQUEST)
        
class ClientTrackOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({'erorr':'The order does not found!'},status=status.HTTP_404_NOT_FOUND)
        data={
            'id':order.id,
            'status':order.status,
            'date':order.orderDate
        }
        return Response(data,status=status.HTTP_200_OK)

        
                
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