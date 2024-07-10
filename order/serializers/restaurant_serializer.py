from rest_framework import serializers
from ..models import Order, OrderItem, OrderAccessory
from restaurant.serializers.products_serializers import ProductListSerializer
from restaurant.models import Product


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


         
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    client=serializers.CharField(source='client.fullName')
    class Meta:
        model = Order
        fields = (
            'id','client','payment', 'status','tax', 'orderDate', 'total_price','total_products','price_with_tax', 'price_with_tax_with_coupon','items'
        )        

class OrderListSerializer(serializers.ModelSerializer):
    client=serializers.CharField(source='client.fullName')
    client_avatar=serializers.CharField(source='client.avatar')
    
    class Meta:
        model = Order
        fields = (
            'id','client', 'orderDate','totalAmount','client_avatar'
        )        
