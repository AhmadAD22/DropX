from rest_framework import serializers
from ..models import Product,AccessoryProduct
from .category_serializers import *

class ProductSerializer(serializers.ModelSerializer):
    price_after_offer = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Product
        fields = ('id','image','category', 'name', 'description', 'price', 'offers', 'quantity', 'minimumOrder', 'created_at', 'updated_on', 'price_after_offer')
        read_only_fields = ('id', 'created_at', 'updated_on')
from rest_framework import serializers

class AccessoryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessoryProduct
        fields = ('id', 'name', 'price', 'quantity')
        
class CreateAccessoryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessoryProduct
        fields = ('id','product' ,'name', 'price', 'quantity')


class CreateListProductSerializer(serializers.ModelSerializer):
    accessory_products = serializers.SerializerMethodField()
    category_name=serializers.CharField(source='category.name',read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
    
    

    class Meta:
        model = Product
        fields = ('id', 'image','category', 'category_name','name', 'description', 'price', 'offers', 'quantity', 'minimumOrder', 'created_at', 'updated_on', 'price_after_offer', 'accessory_products')
        
    def get_accessory_products(self, obj):
        product_accessory=AccessoryProduct.objects.filter(product=obj)
        return AccessoryProductSerializer(product_accessory, many=True).data
    
    
    def create(self, validated_data):
        accessory_products_data = self.context.get('request').data.get('accessory_products', [])
        product = Product.objects.create(**validated_data)
        
        for accessory_data in accessory_products_data:
            accessory_product = AccessoryProduct.objects.create(product=product, **accessory_data)
        
        return product
    def update(self, instance, validated_data):
        accessory_products_data = self.context.get('request').data.get('accessory_products', [])
        
        for field, value in validated_data.items():
            setattr(instance, field, value)
        
        instance.save()
        
        instance.accessory_products.all().delete()
        
        for accessory_data in accessory_products_data:
            accessory_product = AccessoryProduct.objects.create(product=instance, **accessory_data)
        
        return instance
