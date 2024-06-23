from rest_framework import serializers
from ..models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'image', 'created_at', 'updated_on')
        read_only_fields = ('id', 'created_at', 'updated_on')