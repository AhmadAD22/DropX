from rest_framework import serializers
from ..models import *
from rest_framework import fields
from utils.validators import phoneValidator

class PendingDriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingDriver
        exclude=['otp','oldPhone']
        
class UpdateDriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingDriver
        fields = [
            'id', 'avatar', 'gender', 'idNumber', 'birth', 'fullName', 'nationality', 'email',
            'phone', 'latitude', 'longitude', 'address', 'bankName', 'iban', 'companyName',
            'car', 'carName', 'carCategory', 'carColor', 'carLicense', 'drivingLicense',
            'carFront', 'carBack','oldPhone'
        ]
        
class OrderServiceSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderServiceSubscription
        fields = ['id', 'duration', 'price']

class MembersServiceSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembersServiceSubscription
        fields = ['id', 'duration', 'price']
        
class DeiverSerializer(serializers.ModelSerializer):
    car=serializers.StringRelatedField(source='car.carType')
    orderSubscription = OrderServiceSubscriptionSerializer()
    memberSubscription = MembersServiceSubscriptionSerializer()
    class Meta:
        model=Driver
        fields = [
            'id', 'avatar', 'gender', 'idNumber', 'birth', 'fullName', 'nationality', 'email',
            'phone', 'latitude', 'longitude', 'address', 'bankName', 'iban', 'companyName',
            'car', 'carName', 'carCategory', 'carColor', 'carLicense', 'drivingLicense',
            'carFront', 'carBack', 'memberSubscription', 'orderSubscription',
        ]