from rest_framework import serializers
from ..models import *


class RestaurantSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model=RestaurantSubscription
        fields = ['id', 'duration', 'price']

class RestaurantSerializer(serializers.ModelSerializer):
    restaurantSubscription=RestaurantSubscriptionSerializer()
    class Meta:
        model=Restaurant
        fields = [
            'id', 'gender','restaurantStatus' ,'idNumber', 'birth', 'fullName', 'nationality', 'email', 'phone', 'latitude',
            'longitude', 'address', 'bankName', 'iban', 'restaurantName', 'restaurantLogo',
            'commercialRecordNumber', 'commercialRecordImage', 'restaurantSubscription'
        ]
        

class PendingRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingRestaurant
        exclude=['otp','oldPhone']


        
class UpdateRestaurantSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PendingRestaurant
        fields = [
            'id', 'gender', 'idNumber', 'birth', 'fullName', 'nationality', 'email', 'phone', 'latitude',
            'longitude', 'address', 'bankName', 'iban', 'restaurantName', 'restaurantLogo',
            'commercialRecordNumber', 'commercialRecordImage',  'oldPhone'
        ]