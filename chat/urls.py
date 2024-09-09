from django.urls import path, include
from chat import views as chat_views
from django.contrib.auth.views import LoginView, LogoutView
from .views import *

urlpatterns = [
    path("", chat_views.chat_rooms_view, name="chat-page"),
    path('<int:room_id>/', chat_room, name='chat_room'),
    path('api/rooms/', ChatRoomListView.as_view(), name='chatroom-list'),  # List and create chat rooms

    # login-section
    path("auth/login/", LoginView.as_view(template_name="LoginPage.html"), name="login-user"),
    path("auth/logout/", LogoutView.as_view(), name="logout-user"),
]