from rest_framework import serializers
from .models import ChatRoom, Message


# Serializer for the Message model
class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.fullName', read_only=True)  # Include sender's username
    sender_image=serializers.FileField(source='sender.avatar')

    class Meta:
        model = Message
        fields = ['id', 'sender','sender_image', 'sender_name', 'content', 'timestamp']

# Serializer for the ChatRoom model
class ChatRoomSerializer(serializers.ModelSerializer):
    messages=MessageSerializer(many=True)
    class Meta:
        model = ChatRoom
        fields = ['id', 'messages']

