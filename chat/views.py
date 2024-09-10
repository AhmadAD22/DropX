from django.shortcuts import render, redirect,get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import ChatRoom
from .serializers import ChatRoomSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import ChatRoom
from django.db.models import Max
from utils.decerators import staff_member_required
from django.contrib.auth.decorators import permission_required



@permission_required("accounts.Support", raise_exception=True)
@staff_member_required
def chat_rooms_view(request):
    chat_rooms = ChatRoom.objects.annotate(latest_message_time=Max('messages__timestamp')).order_by('-latest_message_time')
    return render(request, 'chat_rooms.html', {'chat_rooms': chat_rooms})


@permission_required("accounts.Support", raise_exception=True)
@staff_member_required
def chat_room(request, room_id):
    room=get_object_or_404(ChatRoom,id=room_id)
    return render(request, 'room.html', {'room': room})


class ChatRoomListView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access

    def get(self, request):
        # Return all chat rooms associated with the authenticated user
        chat_room, _ = ChatRoom.objects.get_or_create(
            user=request.user,
            defaults={'created_at': timezone.now()} 
        )
        serializer = ChatRoomSerializer(chat_room)
        return Response(serializer.data)

