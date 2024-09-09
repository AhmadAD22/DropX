from .models import ChatRoom, Message
from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # Get the room_id from the URL route (e.g., ws/chat/<room_id>/)
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        print(self.room_group_name)
        # Authenticate the user (make sure user is logged in)
        if self.scope["user"].is_anonymous:
            await self.close()  # Close the connection if the user is not authenticated
        else:
            # Join the room group (to broadcast messages to all users in the group)
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            # Accept the WebSocket connection
            await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group when the WebSocket disconnects
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']
        
        # Get the chat room instance
        room = await sync_to_async(ChatRoom.objects.get)(id=self.room_id)
        
        # Get the sender (the currently connected user)
        sender = self.scope['user'].id  # or use a unique identifier
        # Save the message to the database
        await sync_to_async(Message.objects.create)(
            room=room,
            sender=self.scope['user'],
            content=message_content
        )
        
        # Broadcast the message to all users in the WebSocket room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_content,
                'sender': sender
            }
        )

    # This method handles broadcasting the message to the WebSocket
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        current_time = timezone.now().strftime('%H:%M')  # Format time as a string
        current_date = timezone.now().strftime('%Y-%m-%d')  # Format date as a string
        
        # Send the message to WebSocket (frontend)
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'time': current_time,
            'date': current_date
        }))