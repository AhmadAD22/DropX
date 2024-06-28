from utils.sms import SmsSender
from ..models import *
from ..serializers import *
from ..serializers.common_serializer import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from utils.error_handle import error_handler
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class PhoneVerifyView(APIView):
    authentication_classes = []  # Disable authentication
    permission_classes = []  # Disable permission checks
    def post(self,request,*args,**kwargs):
    
        if PhoneVitrifactionSerializer(data=request.data).is_valid(raise_exception=True):
            otp=OTPRequest.objects.filter(phone=request.data['phone'],
                                        code=request.data['code'],
                                        isUsed=False,
                                        type=OTPRequest.Types.REGISTER).first()
            if otp:
                otp.isUsed=True
                return Response({"result":"OTP is correct"})
            else:
                return Response({"error":"OTP is not correct!"},status.HTTP_404_NOT_FOUND)
            
            
class ResetPhoneVerifyView(APIView):
    permission_classes = [IsAuthenticated]  
    def post(self,request,*args,**kwargs):
    
        if PhoneVitrifactionSerializer(data=request.data).is_valid(raise_exception=True):
            otp=OTPRequest.objects.filter(phone=request.data['phone'],
                                        code=request.data['code'],
                                        isUsed=False,
                                        type=OTPRequest.Types.RESET_PHONE).first()
            if otp:
                otp.isUsed=True
                return Response({"result":"OTP is correct,"})
            else:
                return Response({"error":"OTP is not correct!"},status.HTTP_404_NOT_FOUND)


class ForgetPasswordAPIView(APIView):
    permission_classes=[]
    authentication_classes=[]
    def post(self,request,*args, **kwargs):
        
        phone=request.data['phone']
        try:
            user=User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response({"error":"the account not found"},status=status.HTTP_409_CONFLICT)
        if OTPRequest.checkRateLimitReached(phone=phone):
            return Response({'error': 'MANY_OTP_REQUESTS'}, status=status.HTTP_409_CONFLICT)
        otp=OTPRequest.objects.create(phone=phone,type=OTPRequest.Types.FORGET_PASSWORD)
        
            
        sms = SmsSender()
        if sms.send_otp(phone.replace('0', '966', 1), f"Your OTP for Update Your Password is: {otp}"):
                return Response({"result":"Wait to recive an OTP message"}, status=status.HTTP_201_CREATED)
        else:
                return Response({'error': 'Failed to send OTP", "SMS_SEND_FAILED'}, status=status.HTTP_502_BAD_GATEWAY)
        
class ForgetPsswordVerifyPhoneAPIView(APIView):
    permission_classes=[]
    authentication_classes=[]
    def post(self,request,*args, **kwargs):
        otp=OTPRequest.objects.filter(phone=request.data['phone'],
                                        code=request.data['code'],
                                        isUsed=False,
                                        type=OTPRequest.Types.FORGET_PASSWORD).first()
        if otp:
            otp.isUsed=True
            return Response({"result":"OTP is correct"},status.HTTP_200_OK)
        else:
            return Response({"error":"OTP is not correct!"},status.HTTP_404_NOT_FOUND)



class UpdateForgottenPasswordAPIView(APIView):
    permission_classes=[]
    authentication_classes=[]
    def post(self,request,*args, **kwargs):
        try:
            phone=request.data['phone']
            new_password=request.data['password']
            user=User.objects.get(phone=phone)
            # Update the password
            user.set_password(new_password)
            user.save()
            return Response({"result":"Password updated successfully"},status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"erorr":"user does not found"},status.HTTP_404_NOT_FOUND)



class UserPasswordUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        try:
            serializer = UserPasswordUpdateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = request.user
            old_password = serializer.validated_data.get('old_password')
            new_password = serializer.validated_data.get('new_password')

            # Check if the old password is correct
            if not user.check_password(old_password):
                return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)

            # Update the password
            user.set_password(new_password)
            user.save()

            return Response({'detail': 'Password updated successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        
        
    
    