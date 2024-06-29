from rest_framework import serializers
from ..models import Order, OrderItem, OrderAccessory


class OrderAccessorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAccessory
        fields = ('accessory_product', 'quantity', 'unitPrice', 'get_total_price')


class OrderItemSerializer(serializers.ModelSerializer):
    accessories = OrderAccessorySerializer(many=True)

    class Meta:
        model = OrderItem
        fields = ('product', 'quantity', 'unitPrice', 'discount', 'note','get_total_price', 'accessories')


# class OrderSerializer(serializers.ModelSerializer):
#     items = OrderItemSerializer(many=True)

#     class Meta:
#         model = Order
#         fields = (
#             'client', 'deiver', 'restaurantLat', 'restaurantLng', 'restaurantAddress',
#             'destinationLat', 'destinationLng', 'destinationAddress', 'driverLat', 'driverLng',
#             'payment', 'status', 'orderDate', 'deliveryDate',  'totalAmount', 'coupon', 'items'
#         )
   
         
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    client=serializers.CharField(source='client.fullName')
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
            'destinationLat', 'destinationLng', 'destinationAddress','totalAmount',
        )        
