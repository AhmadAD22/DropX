from ..models import *
from ..serializers.common_serializer import*
from ..serializers.restaurant_serializers import *
from ..serializers.driver_serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from utils.error_handle import error_handler
from utils.sms import SmsSender
from django.contrib.auth.hashers import make_password


class AdminAprovalDriverUpdateRequestAPIView(APIView):
    
    def get(self, request):
        updateRequests = PendingDriver.objects.filter(oldPhone__isnull=False)
        serializer = UpdateDriverSerializer(updateRequests, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        pendingDriverId=request.data['pendingDriverId']
        try:
          pending_driver = PendingDriver.objects.get(id=pendingDriverId)
        except PendingDriver.DoesNotExist:
            return Response({'error': 'New Driver data not found'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
          driver = Driver.objects.get(phone=pending_driver.oldPhone)
        except Driver.DoesNotExist:
            return Response({'error': 'Driver  not found'}, status=status.HTTP_404_NOT_FOUND)
        try:   
            driver.fullName=pending_driver.fullName
            driver.avatar=pending_driver.avatar
            driver.phone=pending_driver.phone
            driver.email=pending_driver.email
            driver.gender=pending_driver.gender
            driver.idNumber=pending_driver.idNumber
            driver.birth=pending_driver.birth
            driver.nationality=pending_driver.nationality
            driver.latitude=pending_driver.latitude
            driver.longitude=pending_driver.longitude
            driver.address=pending_driver.address
            driver.bankName=pending_driver.bankName
            driver.iban=pending_driver.iban
            driver.companyName=pending_driver.companyName
            driver.car=pending_driver.car
            driver.carName=pending_driver.carName
            driver.carCategory=pending_driver.carCategory
            driver.carModel=pending_driver.carModel
            driver.carColor=pending_driver.carColor
            driver.carLicense=pending_driver.carLicense
            driver.drivingLicense=pending_driver.drivingLicense
            driver.carFront=pending_driver.carFront
            driver.carBack=pending_driver.carBack
            driver.save(e)
            pending_driver.delete()
        except Exception as e:
            return Response(error_handler(e), status=status.HTTP_400_BAD_REQUEST)
        return Response({'result': 'Driver Updated successfully'}, status=status.HTTP_404_NOT_FOUND)
    def delete(self, request):
        pendingDriverId=request.data['pendingDriverId']
        try:
          pending_driver = PendingDriver.objects.get(id=pendingDriverId)
          pending_driver.delete()
          return Response({'result': 'New driver data deleted successfully'}, status=status.HTTP_404_NOT_FOUND)
        except PendingDriver.DoesNotExist:
            return Response({'error': 'New Driver data not found'}, status=status.HTTP_404_NOT_FOUND)


class AdminAprovalRestaurantUpdateRequestAPIView(APIView):
    
    def get(self, request):
        updateRequests = PendingRestaurant.objects.filter(oldPhone__isnull=False)
        serializer = UpdateRestaurantSerializer(updateRequests, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        pendingRestaurantId=request.data['pendingRestaurantId']
        try:
          pendingRestaurant = PendingRestaurant.objects.get(id=pendingRestaurantId)
        except PendingRestaurant.DoesNotExist:
            return Response({'error': 'New Driver data not found'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
          restaurant = Restaurant.objects.get(phone=pendingRestaurant.oldPhone)
        except Restaurant.DoesNotExist:
            return Response({'error': 'Driver  not found'}, status=status.HTTP_404_NOT_FOUND)
        try:   
            restaurant.fullName=pendingRestaurant.fullName
            restaurant.phone=pendingRestaurant.phone
            restaurant.email=pendingRestaurant.email
            restaurant.gender=pendingRestaurant.gender
            restaurant.idNumber=pendingRestaurant.idNumber
            restaurant.birth=pendingRestaurant.birth
            restaurant.nationality=pendingRestaurant.nationality
            restaurant.latitude=pendingRestaurant.latitude
            restaurant.longitude=pendingRestaurant.longitude
            restaurant.address=pendingRestaurant.address
            restaurant.bankName=pendingRestaurant.bankName
            restaurant.iban=pendingRestaurant.iban
            restaurant.commercialRecordNumber=pendingRestaurant.commercialRecordNumber
            restaurant.restaurantName=pendingRestaurant.restaurantName
            restaurant.commercialRecordImage=pendingRestaurant.commercialRecordImage
            restaurant.restaurantLogo=pendingRestaurant.restaurantLogo
            restaurant.save()
            pendingRestaurant.delete()
        except Exception as e:
            return Response({"error":e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'result': 'Driver Updated successfully'}, status=status.HTTP_404_NOT_FOUND)
    def delete(self, request):
        pendingRestaurantId=request.data['pendingRestaurantId']
        try:
          pendingRestaurant = PendingRestaurant.objects.get(id=pendingRestaurantId)
          pendingRestaurant.delete()
          return Response({'result': 'New Restaurant data deleted successfully'}, status=status.HTTP_404_NOT_FOUND)
        except PendingDriver.DoesNotExist:
            return Response({'error': 'New Restaurant data not found'}, status=status.HTTP_404_NOT_FOUND)

    
