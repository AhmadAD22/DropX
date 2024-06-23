from rest_framework import serializers
from ..models import *
from rest_framework import serializers
from rest_framework import fields
from utils.validators import phoneValidator


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['avatar','phone', 'fullName', 'email',]
        
        

class PendingClientSerializer(serializers.ModelSerializer):
    phone=fields.CharField(validators=[phoneValidator])
    class Meta:
        model=PendingClient
        exclude=['otp']
        
       
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id','avatar','email','fullName', 'phone']


class ClientCreateAccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})


    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)
        return super().create(validated_data)
    
    class Meta:
        model = Client
        fields = ['id', 'fullName', 'avatar','email', 'phone', 'password']
        extra_kwargs = {
            'username': {'required': False}
        }

class ClientPasswordUpdateSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)


class ClientAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['latitude','longitude','address']