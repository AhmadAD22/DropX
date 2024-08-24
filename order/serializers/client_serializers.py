from rest_framework import serializers
from ..models import *


class OrderAccessorySerializer(serializers.ModelSerializer):
    accessory_product=serializers.CharField(source='accessory_product.name',read_only=True)
    class Meta:
        model = OrderAccessory
        fields = ('accessory_product', 'quantity', 'unitPrice', 'get_total_price')

class ProductOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id','image','name',)
        read_only_fields = ('id',)
        
class OrderItemSerializer(serializers.ModelSerializer):
    accessories = OrderAccessorySerializer(many=True)
    product=ProductOrderSerializer()

    class Meta:
        model = OrderItem
        fields = ('product', 'quantity', 'unitPrice',  'note','get_total_price', 'accessories')


         
class ClientOrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = (
            'id','destinationName','destinationPhone','destinationAddress',
            'destinationLng','destinationLat',
            'deliveryDate', 'status','tax',
            'commission', 'orderDate',
            'total_price','deliveryCost',
            'total_products','price_with_tax',
            'price_with_tax_with_coupon','items'
        )    


class OrderListSerializer(serializers.ModelSerializer):
    restaurant_name=serializers.SerializerMethodField(read_only=True)
    def get_restaurant_name(self,obj):
        item=OrderItem.objects.filter(order=obj).first()
        if item:
            return item.product.restaurant.restaurantName
        return None
    class Meta:
        model=Order
        fields=['id','destinationLng','destinationLat','destinationAddress','restaurant_name','deliveryDate','totalAmount','status']
        
class TripCarSerializer(serializers.ModelSerializer):
    trip_time = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    distance=serializers.SerializerMethodField()

    class Meta:
        model = TripCar
        fields = ('id', 'image','car_category','distance','trip_time', 'price')
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
            'car','distance', 'commission','price', 'coupon','tax','price_with_tax','price_with_tax_with_coupon',
        )
        read_only_fields = ('price_with_tax', 'price_with_tax_with_coupon')