from rest_framework import serializers
from accounts.models import *
from restaurant.models import *
from django.utils import timezone


class RestaurantOpeningSerializer(serializers.ModelSerializer):
    class Meta:
        model=RestaurantOpening
        exclude=['restaurant','created_at','updated_on',]




class RestuarantDetailsSerializer(serializers.ModelSerializer):
    openings=serializers.SerializerMethodField()
    def get_openings(self, obj):
        # Customize the serialization of 'openings' field here
        return RestaurantOpeningSerializer(obj.restaurantopening_set.all(), many=True).data

    class Meta:
        model=Restaurant
        fields=['id','restaurantName','restaurantLogo','latitude', 'longitude', 
             'address','phone','description','openings',]
    