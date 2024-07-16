from rest_framework import serializers
from accounts.models import *
from restaurant.models import *
from django.utils import timezone
from restaurant.serializers.products_serializers import ProductListSerializer
from restaurant.serializers.category_serializers import CategorySerializer
from restaurant.serializers.store_serializers import *
from django.db.models import Avg, Count


class RestaurantOpeningSerializer(serializers.ModelSerializer):
    class Meta:
        model=RestaurantOpening
        exclude=['restaurant','created_at','updated_on',]


class RestaurantListSerializer(serializers.ModelSerializer):
    reviews_average = serializers.SerializerMethodField(read_only=True)
    reviews_count = serializers.SerializerMethodField(read_only=True)
    def get_reviews_count(self, obj):
        return obj.restaurantreview.aggregate(count=Count('id')).get('count')
    def get_reviews_average(self, obj):
        average_rating = obj.restaurantreview.aggregate(avg_rating=Avg('rating')).get('avg_rating')
        return average_rating if average_rating else 0
    class Meta:
        model=Restaurant
        fields=['id','restaurantName','restaurantLogo','latitude', 'longitude', 
             'address','reviews_count','reviews_average']


class RestuarantDetailsSerializer(serializers.ModelSerializer):
    openings=serializers.SerializerMethodField()
    products=serializers.SerializerMethodField()
    categories=serializers.SerializerMethodField()
    reviews=serializers.SerializerMethodField()
    reviews_average = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    commonquestion=serializers.SerializerMethodField()
    def get_openings(self, obj):
        # Customize the serialization of 'openings' field here
        return RestaurantOpeningSerializer(obj.restaurantopening_set.all(), many=True).data
    def get_reviews(self, obj):
        # Customize the serialization of 'openings' field here
        return ReviewsStorSerializer(obj.restaurantreview.all(), many=True).data
    def get_commonquestion(self, obj):
        # Customize the serialization of 'openings' field here
        return CommonQuestionSerializer(obj.restaurantcommonquestion.all(), many=True).data
    def get_reviews_average(self, obj):
        average_rating = obj.restaurantreview.aggregate(avg_rating=Avg('rating')).get('avg_rating')
        return average_rating if average_rating else 0
    def get_products(self, obj):
        products=Product.objects.filter(restaurant=obj)
        return ProductListSerializer(products, many=True).data
    def get_reviews_count(self, obj):
        return obj.restaurantreview.aggregate(count=Count('id')).get('count')
    def get_categories(self, obj):
        products=Product.objects.filter(restaurant=obj)
        categories = Category.objects.filter(productCategory__in=products).distinct()
        return CategorySerializer(categories, many=True).data



    class Meta:
        model=Restaurant
        fields=['id','restaurantName','restaurantLogo','latitude', 'longitude', 
             'address','phone','description','openings','categories','products',
             'reviews','reviews_average','reviews_count','commonquestion']
    
    
class RestaurantReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model=RestaurantReview
        exclude=['client','restaurant']