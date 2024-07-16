from rest_framework import serializers
from ..models import *
from restaurant.serializers.products_serializers import ProductListSerializer,ProductReviewsSerializer
from django.db.models import Avg, Count


class FavoriteProductSerializer(serializers.ModelSerializer):
    product=ProductListSerializer(read_only=True)

    class Meta:
        model = FavoriteProduct
        fields = ['product']
        

# class ProductReviewsSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = FavoriteProduct
#         fields = ['product']
        
class AccessoryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessoryProduct
        fields = ('id', 'name', 'price', 'quantity')
        
class ProductSerializer(serializers.ModelSerializer):
    price_after_offer = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    accessories=serializers.SerializerMethodField()
    restaurant_name=serializers.CharField(source="restaurant.restaurantName",read_only=True)
    restaurant_avatar=serializers.FileField(source="restaurant.avatar",read_only=True)
    reviews_average = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    reviews=serializers.SerializerMethodField()
    def get_accessories(self, obj):
        accessories=AccessoryProduct.objects.filter(product=obj)
        return AccessoryProductSerializer(accessories, many=True).data
    def get_reviews_average(self, product):
        average_rating = product.productreview.aggregate(avg_rating=Avg('rating')).get('avg_rating')
        return average_rating if average_rating else 0

    def get_reviews_count(self, product):
        return product.productreview.aggregate(count=Count('id')).get('count')
    def get_reviews(self, obj):
        reviews=ProductReview.objects.filter(product=obj)
        return ProductReviewsSerializer(reviews, many=True).data
    
    class Meta:
        model = Product
        fields = ('id','image','restaurant_name','restaurant_avatar', 'name', 'description', 'price', 'offers','price_after_offer', 'quantity', 'accessories', 'reviews_average', 'reviews_count','reviews')
        read_only_fields = ('id',)