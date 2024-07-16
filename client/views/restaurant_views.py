from rest_framework.response import Response
from rest_framework.views import APIView
from utils.error_handle import error_handler
from ..serializers.restaurant_serializer import *
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from geopy.distance import geodesic
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.restaurant_serializer import *
from utils.geographic import get_nearest_restaurants

class NearestRestaurantsAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        client_latitude = request.user.latitude
        client_longitude = request.user.longitude

        if client_latitude is None or client_longitude is None:
            return Response({'error': 'Latitude and longitude parameters are required.'}, status=400)
        restaurants = Restaurant.objects.filter(restaurantStatus=True)
        nearest_restaurants=get_nearest_restaurants(client_latitude=client_latitude,client_longitude=client_longitude,restaurants=restaurants)
        
        return Response(nearest_restaurants)


class RestaurantDatailsApiVew(APIView):
    permission_classes=[IsAuthenticated]
    def get (self,request,*args, **kwargs):
        try:
         restaurant=Restaurant.objects.get(pk=kwargs['restaurant_id'])
        except Restaurant.DoesNotExist:
            return Response({"error":"Restaurant does not found"},status=status.HTTP_404_NOT_FOUND)
        restaurantSerializer=RestuarantDetailsSerializer(restaurant)
        return Response(restaurantSerializer.data,status=status.HTTP_200_OK)
    

class RestaurantReviewsAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        restaurant_id=request.data['restaurant_id']
        try:
            client=Client.objects.get(phone=request.user.phone)
        except Client.DoesNotExist:
            return Response({"error":"Client does not found"},status=status.HTTP_404_NOT_FOUND)
        try:
         restaurant=Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:
            return Response({"error":"Restaurant does not found"},status=status.HTTP_404_NOT_FOUND)
        review_serializer=RestaurantReviewsSerializer(data=request.data)
        if review_serializer.is_valid():
            review_serializer.save(client=client,restaurant=restaurant)
            return Response(review_serializer.data,status=status.HTTP_200_OK)
        return Response(error_handler(review_serializer.errors),status=status.HTTP_404_NOT_FOUND)
            
        