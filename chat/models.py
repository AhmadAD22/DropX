from django.db import models
from accounts.models import User
from django.utils import timezone

# Chat Room model to represent the chat session between a user and support agent
class ChatRoom(models.Model):
    # Optional if you have agents; otherwise, just one user field would work
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_rooms')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat Room {self.id} - {self.user.username}"

# Message model for storing individual chat messages
class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)  # The sender of the message (can be user or agent)
    content = models.TextField()  # The chat message itself
    timestamp = models.DateTimeField(default=timezone.now)  # When the message was sent

    def __str__(self):
        return f"Message from {self.sender.username} in room {self.room.id}"

    class Meta:
        ordering = ['timestamp']  # Sort messages by the time they were sent
