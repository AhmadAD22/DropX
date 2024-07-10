from rest_framework import serializers
from ..models import *
from restaurant.serializers.products_serializers import ProductListSerializer

class FavoriteProductSerializer(serializers.ModelSerializer):
    product=ProductListSerializer(read_only=True)

    class Meta:
        model = FavoriteProduct
        fields = ['product']