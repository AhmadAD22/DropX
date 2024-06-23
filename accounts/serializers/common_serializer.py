from rest_framework import serializers
from ..models import *
from rest_framework import serializers
from rest_framework import fields
from utils.validators import phoneValidator


class PhoneVitrifactionSerializer(serializers.Serializer):
    phone=fields.CharField(validators=[phoneValidator])
    code=fields.CharField()


class PhoneAuthTokenSerializer(serializers.Serializer):
    phone = serializers.CharField(validators=[phoneValidator])
    password = serializers.CharField()

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')

        if phone and password:
            return attrs
        raise serializers.ValidationError('Phone and password are required.')
    
class UserPasswordUpdateSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    
    
