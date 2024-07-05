from rest_framework import serializers
from ..models import Product,AccessoryProduct
from .category_serializers import *

class ProductSerializer(serializers.ModelSerializer):
    price_after_offer = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Product
        fields = ('id','image','category', 'name', 'description', 'price', 'offers', 'quantity', 'minimumOrder', 'created_at', 'updated_on', 'price_after_offer')
        read_only_fields = ('id', 'created_at', 'updated_on')
        
from django.db.models import Avg, Count

class ProductListSerializer(serializers.ModelSerializer):
    price_after_offer = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    reviews_average = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    def get_reviews_average(self, product):
        average_rating = product.productreview.aggregate(avg_rating=Avg('rating')).get('avg_rating')
        return average_rating if average_rating else 0

    def get_reviews_count(self, product):
        return product.productreview.aggregate(count=Count('id')).get('count')

    class Meta:
        model = Product
        fields = ('id', 'image', 'name', 'description', 'minimumOrder','price', 'offers', 'created_at', 'quantity','updated_on', 'price_after_offer', 'reviews_average', 'reviews_count')
        read_only_fields = ('id', 'created_at', 'updated_on')

class AccessoryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessoryProduct
        fields = ('id', 'name', 'price', 'quantity')
        
class CreateAccessoryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessoryProduct
        fields = ('id' ,'name', 'price', 'quantity')


class CreateListProductSerializer(serializers.ModelSerializer):
    category_name=serializers.CharField(source='category.name',read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
    
    

    class Meta:
        model = Product
        fields = ('id', 'image','category', 'category_name','name', 'description', 'price', 'offers', 'quantity', 'minimumOrder', 'created_at', 'updated_on', 'price_after_offer')
        
    
    
    def update(self, instance, validated_data):
        accessory_products_data = self.context.get('request').data.get('accessory_products', [])
        
        for field, value in validated_data.items():
            setattr(instance, field, value)
        
        instance.save()
        
        instance.accessory_products.all().delete()
        
        for accessory_data in accessory_products_data:
            accessory_product = AccessoryProduct.objects.create(product=instance, **accessory_data)
        
        return instance
