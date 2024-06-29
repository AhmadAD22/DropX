from rest_framework import serializers
from accounts.models import *
from ..models import *
from .category_serializers import *
from accounts.serializers.client_serializers import ClientSerializer

class RestaurantOpeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantOpening
        fields = ('id' ,'day', 'time_start', 'time_end', 'Rest_time_start', 'Rest_time_end')

class CommonQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonQuestion
        fields = ('id',  'question', 'answer')


class RestaurantDataSerializer(serializers.ModelSerializer):
    openings = serializers.SerializerMethodField(read_only=True)
    commonQuestions = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=Restaurant
        fields=['restaurantLogo','restaurantName','description','address','longitude','latitude','openings','commonQuestions',]
        
    def get_commonQuestions(self, obj):
        # Customize the serialization of 'Common question' field here
        return CommonQuestionSerializer(obj.commonquestion_set.all(), many=True).data
        
    def get_openings(self, obj):
        # Customize the serialization of 'Common question' field here
        return RestaurantOpeningSerializer(obj.restaurantopening_set.all(), many=True).data
    
class ReviewsStorSerializer(serializers.ModelSerializer):
    Client=ClientSerializer(read_only=True)
    class Meta:
        model = ProductReview
        exclude = ['product']
    