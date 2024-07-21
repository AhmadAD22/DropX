from rest_framework import serializers
from ..models import Cart, CartItem, CartAccessory,OrderConfig
from restaurant.models import AccessoryProduct,Product

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
        
class ProductSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = Product
            fields = ('id','image','category', 'name', 'price', 'offers', 'price_after_offer')
            read_only_fields = ('id', )
            
class AccessoryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessoryProduct
        fields = ('id', 'name', 'price')

class CartAccessorySerializer(serializers.ModelSerializer):
    accessory_product=AccessoryProductSerializer(read_only=True)
    class Meta:
        
        model = CartAccessory
        fields = ['id', 'accessory_product', 'quantity','accessory_total_price']


class CartItemSerializer(serializers.ModelSerializer):
    accessories = CartAccessorySerializer(many=True)
    product=ProductSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'note', 'accessories','item_total_price','item_with_accessories_total_price']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']
        
class CartCheckoutSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    client_name=serializers.CharField(source='client.fullName',read_only=True)
    client_phone=serializers.CharField(source='client.phone',read_only=True)
    client_address=serializers.CharField(source='client.address',read_only=True)
    client_latitude=serializers.CharField(source='client.latitude',read_only=True)
    client_longitude=serializers.CharField(source='client.longitude',read_only=True)
        

    class Meta:
        model = Cart
        fields = ['id','client_name' ,'client_phone','client_latitude','client_longitude','client_address','items','tax','total_price','total_price_with_tax']
        
        