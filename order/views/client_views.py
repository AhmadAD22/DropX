from rest_framework.views import APIView
from ..models import *
from ..serializers.client_serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from accounts.models import Client

from utils.geographic import calculate_distance
class TripCarAPIView(APIView):
    
    def get(self, request, *args, **kwargs):
        car = TripCar.objects.all()
         # Get distance from query parameter
        source_lat = request.query_params.get('source_lat')
        source_lon = request.query_params.get('source_lon')
        destenation_lat = request.query_params.get('destenation_lat')
        destenation_lon = request.query_params.get('destenation_lon')
        distance=calculate_distance(source_lat,source_lon,destenation_lat,destenation_lon)
        serializer = TripCarSerializer(car, context={'distance': distance},many=True)
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
        order.status=Status.CANCELLED
        order.save()
        serializer = ClientOrderSerializer(order)
        return Response(serializer.data)
        