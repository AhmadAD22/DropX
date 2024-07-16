from rest_framework.response import Response
from rest_framework.views import APIView
from utils.error_handle import error_handler
from ..serializers.driver_serializers import *
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.models import Client,Driver



class DriverReviewsAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        driver_id=request.data['driver_id']
        try:
            client=Client.objects.get(phone=request.user.phone)
        except Client.DoesNotExist:
            return Response({"error":"Client does not found"},status=status.HTTP_404_NOT_FOUND)
        try:
         driver=Driver.objects.get(pk=driver_id)
        except Driver.DoesNotExist:
            return Response({"error":"Driver does not found"},status=status.HTTP_404_NOT_FOUND)
        review_serializer=DriverReviewsSerializer(data=request.data)
        if review_serializer.is_valid():
            review_serializer.save(client=client,driver=driver)
            return Response(review_serializer.data,status=status.HTTP_200_OK)
        return Response(error_handler(review_serializer.errors),status=status.HTTP_404_NOT_FOUND)
            