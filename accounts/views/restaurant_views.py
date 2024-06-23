from ..models import *
from ..serializers.common_serializer import*
from ..serializers.restaurant_serializers import *
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

class RestaurantProfileAPIView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request):
        try:
            restaurant = Restaurant.objects.get(phone=request.user.phone)
            serializer = RestaurantSerializer(restaurant)
            return Response(serializer.data)
        except Restaurant.DoesNotExist:
            return Response({'error': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request):
        try:
            restaurant = Restaurant.objects.get(phone=request.user.phone)
            restaurant.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Restaurant.DoesNotExist:
            return Response({'error': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)


class RestaurantAuthToken(ObtainAuthToken):
    permission_classes=[]
    serializer_class = PhoneAuthTokenSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        password = serializer.validated_data['password']
        
        User = get_user_model()
        try:
            user = User.objects.get(phone=phone)
            restaurant = Restaurant.objects.get(phone=user.phone)

        except User.DoesNotExist:
            return Response({'error': 'not a restaurant account'})
        
        if check_password(password, user.password):
            if restaurant.phone == user.phone:
                token, _ = Token.objects.get_or_create(user=user)
                if restaurant.enabled==True:
                    return Response({
                        'token': token.key,
                        'user': {
                            'id': restaurant.id,
                            'phone': restaurant.phone,
                            'email': restaurant.email,
                            
                        }
                    })
                else:
                    return Response({'error': 'Wait for admin acceptance'})
            
        return Response({'error': 'Invalid credentials'})
    

class RestaurantRegisterRequestView(APIView):
    def post(self,request,*args,**kwargs):
        serialized=PendingRestaurantSerializer(data=request.data)
          # check if user exists
        if User.objects.filter(Q(phone=request.data['phone'])|Q(email=request.data['email'])).exists():
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



class RestaurantCreateAccountAPIView(APIView):
    authentication_classes = []  # Disable authentication
    permission_classes = []  # Disable permission checks

    def post(self, request):
        if PhoneVitrifactionSerializer(data=request.data).is_valid(raise_exception=True):
            otp = OTPRequest.objects.filter(phone=request.data['phone'],
                                            code=request.data['code'],                                            
                                            type=OTPRequest.Types.REGISTER).first()
            pendingRestaurant = otp.pendingRestaurant   
            
            if User.objects.filter(Q(phone=pendingRestaurant.phone) | Q(email=pendingRestaurant.email)).exists():
                return Response({'error': 'IDENTIFIER_EXISTS'})

            newRestaurant = Restaurant.objects.create(
                fullName=pendingRestaurant.fullName,
                phone=pendingRestaurant.phone,
                email=pendingRestaurant.email,
                gender=pendingRestaurant.gender,
                idNumber=pendingRestaurant.idNumber,
                birth=pendingRestaurant.birth,
                nationality=pendingRestaurant.nationality,
                latitude=pendingRestaurant.latitude,
                longitude=pendingRestaurant.longitude,
                address=pendingRestaurant.address,
                bankName=pendingRestaurant.bankName,
                iban=pendingRestaurant.iban,
                commercialRecordNumber=pendingRestaurant.commercialRecordNumber,
                restaurantName=pendingRestaurant.restaurantName,
                commercialRecordImage=pendingRestaurant.commercialRecordImage,
                restaurantLogo=pendingRestaurant.restaurantLogo,
                restaurantSubscription=pendingRestaurant.restaurantSubscription,
                fcm_token=request.data['fcm_token']
            )
            newRestaurant.password = make_password(request.data['password'])
            newRestaurant.save()
            pendingRestaurant.delete()
            otp.delete()
            

            return Response({"result": "Restaurant. created successfully"}, status=status.HTTP_201_CREATED)
        return Response({'error': 'The phone is not verified'})
    

class PendingRestaurantRequestUpdateAPIView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request,*args,**kwargs):
        serialized=PendingRestaurantSerializer(data=request.data)
        oldPhone=request.user.phone
        # check if user exists
        if request.data['phone']!=oldPhone:
            if Restaurant.objects.filter(Q(phone=request.data['phone'])|Q(email=request.data['email'])).exists():
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

      