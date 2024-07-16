from rest_framework import serializers
from ..models import Cart, CartItem, CartAccessory
from restaurant.models import AccessoryProduct,Product


        
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