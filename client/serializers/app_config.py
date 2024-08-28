from rest_framework import serializers
from dashboard.models import AppConfig

class AppConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppConfig
        fields = [
            'about', 
            'privacy_policy', 
            'Terms', 
            'twiter', 
            'facebook', 
            'instagram', 
            'youtube', 
            'tiktok', 
            'whatsapp'
        ]