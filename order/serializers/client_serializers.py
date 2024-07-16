from rest_framework import serializers
from ..models import Trip,TripCar



class TripCarSerializer(serializers.ModelSerializer):
    trip_time = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    distance=serializers.SerializerMethodField()

    class Meta:
        model = TripCar
        fields = ('id', 'image','name','distance','trip_time', 'price')
    def get_distance(self, obj):
        return self.context.get('distance')
         
    def get_trip_time(self, obj):
        # Calculate trip time
        distance = self.context.get('distance')
        return obj.trip_time(distance)

    def get_price(self, obj):
        # Calculate price
        distance = self.context.get('distance')
        return obj.price(distance)
    
    
class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = (
            'id', 'note', 'tripDate',
            'sourceLat', 'sourceLng', 'sourceAddress',
            'destinationLat', 'destinationLng', 'destinationAddress',
            'car','distance', 'price', 'coupon','tax','price_with_tax','price_with_tax_with_coupon',
        )
        read_only_fields = ('price_with_tax', 'price_with_tax_with_coupon')