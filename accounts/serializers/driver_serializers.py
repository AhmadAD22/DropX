from rest_framework import serializers
from ..models import *
from rest_framework import fields
from utils.validators import phoneValidator

class PendingDriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingDriver
        exclude=['otp','oldPhone']
        
class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = [
                'id', 'carType'
                ]
            
class UpdateDriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingDriver
        fields = [
            'id', 'avatar', 'gender', 'idNumber', 'birth', 'fullName', 'nationality', 'email',
            'phone', 'latitude', 'longitude', 'address', 'bankName', 'iban', 'companyName',
            'car', 'carName', 'carCategory', 'carColor', 'carLicense', 'drivingLicense',
            'carFront', 'carBack','oldPhone'
        ]
        

class DeiverSerializer(serializers.ModelSerializer):
    car=serializers.StringRelatedField(source='car.carType')
    class Meta:
        model=Driver
        fields = [
            'id', 'avatar', 'gender', 'idNumber', 'birth', 'fullName', 'nationality', 'email',
            'phone', 'latitude', 'longitude', 'address', 'bankName', 'iban', 'companyName',
            'car', 'carName', 'carCategory', 'carColor', 'carLicense', 'drivingLicense',
            'carFront', 'carBack', 'memberSubscription', 'orderSubscription',
        ]
        
        
class OrderSubscriptionSerializer(serializers.ModelSerializer):
    
    remaining_time = serializers.SerializerMethodField()

    class Meta:
        model = DriverOrderSubscription
        fields = ['id', 'duration', 'price', 'start_date','end_date', 'remaining_time']
        
    def get_remaining_time(self, instance):
        return instance.calculate_remaining_time()
    
        
class TripSubscriptionSerializer(serializers.ModelSerializer):
    
    remaining_time = serializers.SerializerMethodField()

    class Meta:
        model = DriverTripSubscription
        fields = ['id', 'duration', 'price', 'start_date','end_date', 'remaining_time']

    
    def get_remaining_time(self, instance):
        return instance.calculate_remaining_time()
    
class DeiverProfileSerializer(serializers.ModelSerializer):
    car=serializers.CharField(source='car.carType')
    driverOrderSubscription=OrderSubscriptionSerializer()
    driverTripSubscription=TripSubscriptionSerializer()
    class Meta:
        model=Driver
        fields = [
            'id', 'avatar', 'gender', 'idNumber', 'birth', 'fullName', 'nationality', 'email',
            'phone', 'latitude', 'longitude', 'address', 'bankName', 'iban', 'companyName',
            'car', 'carName', 'carCategory', 'carColor', 'carLicense', 'drivingLicense',
            'carFront', 'carBack','driverOrderSubscription','driverTripSubscription'
        ]