from rest_framework import serializers
from ..models import *
from datetime import datetime, timedelta


class RestaurantSubscriptionSerializer(serializers.ModelSerializer):
    
    remaining_time = serializers.SerializerMethodField()

    class Meta:
        model = RestaurantSubscription
        fields = ['id', 'duration', 'price', 'start_date','end_date', 'remaining_time']

    
    def get_remaining_time(self, instance):
        return instance.calculate_remaining_time()
    
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