from rest_framework import serializers
from ..models import Order, OrderItem, OrderAccessory,Trip


class OrderAccessorySerializer(serializers.ModelSerializer):
    accessory_product=serializers.CharField(source='accessory_product.name')
    class Meta:
        model = OrderAccessory
        fields = ('accessory_product', 'quantity', 'unitPrice', 'get_total_price')


class OrderItemSerializer(serializers.ModelSerializer):
    accessories = OrderAccessorySerializer(many=True)
    product=serializers.CharField(source='product.name')
    class Meta:
        model = OrderItem
        fields = ('product', 'quantity', 'unitPrice', 'discount', 'note','get_total_price', 'accessories')

class DriverOrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    client_name=serializers.CharField(source='client.fullName')
    client_phone=serializers.CharField(source='client.phone')
    restaurant_name=serializers.SerializerMethodField()
    restaurant_phone=serializers.SerializerMethodField()
    def get_restaurant_name(self,obj):
        return obj.items.first().product.restaurant.restaurantName
    
    def get_restaurant_phone(self,obj):
        return obj.items.first().product.restaurant.phone
    class Meta:
        model = Order
        fields = (
            'id','client_name','client_phone','restaurant_name','restaurant_phone','restaurantLat','restaurantLng','restaurantAddress','destinationName','destinationPhone','destinationAddress',
            'destinationLng','destinationLat',
            'deliveryDate', 'status','tax',
            'commission', 'orderDate',
            'total_price','deliveryCost',
            'total_products','price_with_tax',
            'price_with_tax_with_coupon','items',
            
        )    


         
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = (
            'id','client','payment', 'status', 'orderDate',  'totalAmount','items'
        )        

class DriverOrderListSerializer(serializers.ModelSerializer):
    client=serializers.CharField(source='client.fullName')
    class Meta:
        model = Order
        fields = (
            'id','client', 'orderDate','restaurantLat', 'restaurantLng', 'restaurantAddress',
            'destinationLat', 'destinationLng','status', 'destinationAddress','totalAmount',
        )        


class DriverTripListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = (
            'id', 'tripDate',
            'sourceLat', 'sourceLng', 'sourceAddress',
            'destinationLat', 'destinationLng','status', 'destinationAddress',
            'distance', 'price', 'price_with_tax','price_with_tax_with_coupon',
        )