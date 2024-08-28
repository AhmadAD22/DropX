from rest_framework.response import Response
from rest_framework.views import APIView
from utils.error_handle import error_handler
from ..serializers.driver_serializers import *
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.models import Client,Driver

from dashboard.models import Advertisement
from accounts.models import User
class AdvertisementAPIView(APIView):
    def get(self, request):
        advertisements = Advertisement.objects.filter(active=True).order_by('-created_at')
        images = [ad.image.url for ad in advertisements]
        return Response({'images': images})
    
class ChangeNotificationStatusAPIView(APIView):
    def put(self, request):
        user= request.user 
        if user.notificationEnabled==True:
            user.notificationEnabled=False 
        else:
            user.notificationEnabled=True
        user.save()
        return Response({"notification_enabled": user.notificationEnabled },status=status.HTTP_200_OK)
    def get(self, request):
        return Response({"notification_enabled":request.user.notificationEnabled },status=status.HTTP_200_OK)