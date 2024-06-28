
from ..models import *
from ..serializers.common_serializer import*
from ..serializers.driver_serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from utils.error_handle import error_handler
from utils.sms import SmsSender
from django.contrib.auth.hashers import make_password





class DriverAuthToken(ObtainAuthToken):
    permission_classes=[IsAuthenticated]
    serializer_class = PhoneAuthTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        password = serializer.validated_data['password']
        
        User = get_user_model()
        try:
            user = User.objects.get(phone=phone)
            driver = Driver.objects.get(phone=user.phone)

        except User.DoesNotExist:
            return Response({'error': 'not a driver account'})
        
        if check_password(password, user.password):
            if driver.phone == user.phone:
                token, _ = Token.objects.get_or_create(user=user)
                if driver.enabled==True:
                    return Response({
                        'token': token.key,
                        'user': {
                            'id': driver.id,
                            'phone': driver.phone,
                            'email': driver.email,
                            
                        }
                    })
                else:
                    return Response({'error': 'Wait for admin acceptance'})
            
        return Response({'error': 'Invalid credentials'},status=status.HTTP_409_CONFLICT)
    
    
    
    
    


class DriverProfileAPIView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request):
        try:
            driver = Driver.objects.get(phone=request.user.phone)
            serializer = DeiverSerializer(driver)
            return Response(serializer.data)
        except Driver.DoesNotExist:
            return Response({'error': 'Driver not found'}, status=status.HTTP_404_NOT_FOUND)
    def delete(self, request):
        try:
            driver = Driver.objects.get(phone=request.user.phone)
            driver.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Driver.DoesNotExist:
            return Response({'error': 'Driver not found'}, status=status.HTTP_404_NOT_FOUND)

class DriverRequestUpdateAPIView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request,*args,**kwargs):
        serialized=PendingDriverSerializer(data=request.data)
        oldPhone=request.user.phone
          # check if user exists
        if request.data['phone']!=oldPhone:
            if Driver.objects.filter(Q(phone=request.data['phone'])|Q(email=request.data['email'])).exists():
                return Response({'error': 'Phone number or email already exists'}, status=status.HTTP_409_CONFLICT)
            
            if OTPRequest.checkRateLimitReached(phone=request.data['phone']):
                return Response({'error': 'MANY_OTP_REQUESTS'}, status=status.HTTP_409_CONFLICT)
            if serialized.is_valid():
                otp=OTPRequest.objects.create(phone=request.data['phone'],type=OTPRequest.Types.RESET_PHONE)
                serialized.save(otp=otp,oldPhone=oldPhone) 
                sms = SmsSender()
                if sms.send_otp(request.data['phone'].replace('0', '966', 1), f" Your OTP for registration is: {otp}"):
                    return Response({"result":"Wait to recive OTP"}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': 'Failed to send OTP", "SMS_SEND_FAILED'}, status=status.HTTP_502_BAD_GATEWAY)
            else:
                return Response(error_handler(serialized.errors), status=status.HTTP_400_BAD_REQUEST)
        else:
             if serialized.is_valid():
                serialized.save(oldPhone=oldPhone)
                return Response({"result":"Wait for admin acceptance"}, status=status.HTTP_200_OK)
             else:
                return Response(error_handler(serialized.errors), status=status.HTTP_400_BAD_REQUEST)
        
    


class DreiverRegisterRequestView(APIView):
    def post(self,request,*args,**kwargs):
        serialized=PendingDriverSerializer(data=request.data)
          # check if user exists
        if Driver.objects.filter(Q(phone=request.data['phone'])|Q(email=request.data['email'])).exists():
            return Response({'error': 'Phone number or email already exists'}, status=status.HTTP_409_CONFLICT)
        
        if OTPRequest.checkRateLimitReached(phone=request.data['phone']):
            return Response({'error': 'MANY_OTP_REQUESTS'}, status=status.HTTP_409_CONFLICT)
        if serialized.is_valid():
            otp=OTPRequest.objects.create(phone=request.data['phone'],type=OTPRequest.Types.REGISTER)
            serialized.save(otp=otp) 
            sms = SmsSender()
            if sms.send_otp(request.data['phone'].replace('0', '966', 1), f" Your OTP for registration is: {otp}"):
                return Response({"result":"Wait to recive OTP"}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Failed to send OTP", "SMS_SEND_FAILED'}, status=status.HTTP_502_BAD_GATEWAY)
        else:
            return Response(error_handler(serialized.errors), status=status.HTTP_400_BAD_REQUEST)

class DriverCreateAccountAPIView(APIView):
    authentication_classes = []  # Disable authentication
    permission_classes = []  # Disable permission checks

    def post(self, request):
        if PhoneVitrifactionSerializer(data=request.data).is_valid(raise_exception=True):
            otp = OTPRequest.objects.filter(phone=request.data['phone'],
                                            code=request.data['code'],                                            
                                            type=OTPRequest.Types.REGISTER).first()
            pending_driver = otp.pendingDriver    
            
            if User.objects.filter(Q(phone=pending_driver.phone) | Q(email=pending_driver.email)).exists():
                return Response({'error': 'IDENTIFIER_EXISTS'})

            new_driver = Driver.objects.create(
                fullName=pending_driver.fullName,
                avatar=pending_driver.avatar,
                phone=pending_driver.phone,
                email=pending_driver.email,
                gender=pending_driver.gender,
                idNumber=pending_driver.idNumber,
                birth=pending_driver.birth,
                nationality=pending_driver.nationality,
                latitude=pending_driver.latitude,
                longitude=pending_driver.longitude,
                address=pending_driver.address,
                bankName=pending_driver.bankName,
                iban=pending_driver.iban,
                companyName=pending_driver.companyName,
                car=pending_driver.car,
                carName=pending_driver.carName,
                carCategory=pending_driver.carCategory,
                carModel=pending_driver.carModel,
                carColor=pending_driver.carColor,
                carLicense=pending_driver.carLicense,
                drivingLicense=pending_driver.drivingLicense,
                carFront=pending_driver.carFront,
                carBack=pending_driver.carBack,
                memberSubscription=pending_driver.memberSubscription,
                orderSubscription=pending_driver.orderSubscription,
                fcm_token=request.data['fcm_token']
            )
            print(pending_driver.orderSubscription)
            new_driver.password = make_password(request.data['password'])
            new_driver.save()
            pending_driver.delete()
            otp.delete()

            return Response({"result": "Driver created successfully"}, status=status.HTTP_201_CREATED)
        return Response({'error': 'The phone is not verified'})
      

