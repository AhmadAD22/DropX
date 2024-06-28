from rest_framework.response import Response
from rest_framework.views import APIView
from utils.error_handle import error_handler
from ..serializers.restaurant_serializer import *
from rest_framework import status

class RestaurantDatailsApiVew(APIView):
    
    def get (self,request,*args, **kwargs):
        try:
         restaurant=Restaurant.objects.get(pk=kwargs['restaurant_id'])
        except Restaurant.DoesNotExist:
            return Response({"error":"Restaurant does not found"},status=status.HTTP_404_NOT_FOUND)
        restaurantSerializer=RestuarantDetailsSerializer(restaurant)
        return Response(restaurantSerializer.data,status=status.HTTP_200_OK)
    
class RestaurantDatailsApiVew2(APIView):
    
    def get (self,request,*args, **kwargs):
    
        restaurant=Restaurant.objects.all()
        restaurantSerializer=RestuarantDetailsSerializer(restaurant,many=True)
        return Response(restaurantSerializer.data,status=status.HTTP_200_OK)
