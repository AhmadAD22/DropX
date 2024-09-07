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
from wallet.models import UserWallet,RestaurantSubscriptionPayment
from django.db import IntegrityError


class RestaurantSubscriptionConfigList(APIView):
    authentication_classes = []  # Disable authentication
    permission_classes = []  # Disable permission checks

    def get(self, request):
        subscription_configs = SubscriptionConfig.objects.filter(type="RESTAURANT")
        serializer = SubscriptionConfigSerializer(subscription_configs, many=True)
        return Response(serializer.data)
    
class RestaurantMinimumOrderUpdateAPIView(APIView):
    permission_classes=[IsAuthenticated]

    def put(self, request):
        try:
            restaurant = Restaurant.objects.get(phone=request.user.phone)
            restaurant.minimumOrder=request.data['minimumOrder']
            restaurant.save()
            serializer = RestaurantSerializer(restaurant)
            return Response(serializer.data)
        except Restaurant.DoesNotExist:
            return Response({'error': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)
        
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
    authentication_classes = []  # Disable authentication
    permission_classes = []  # Disable permission checks

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
            return Response({'error': 'not a restaurant account'},status=status.HTTP_404_NOT_FOUND)
        
        if check_password(password, user.password):
            if restaurant.phone == user.phone:
                token, _ = Token.objects.get_or_create(user=user)
                fcm_token=request.data['fcm_token']
                restaurant.fcm_token=fcm_token
                restaurant.save()
                if restaurant.enabled==True:
                    return Response({
                        'token': token.key,
                        'user': {
                            'id': restaurant.id,
                            'phone': restaurant.phone,
                            'email': restaurant.email,
                            'subscription_paid':restaurant.restaurantSubscription.paid
                            
                        }
                    })
                else:
                    return Response({'error': 'Wait for admin acceptance'},status=status.HTTP_409_CONFLICT)
            
        return Response({'error': 'Invalid credentials'},status=status.HTTP_409_CONFLICT)
    

class RestaurantRegisterRequestView(APIView):
    authentication_classes = []  # Disable authentication
    permission_classes = []  # Disable permission checks
    def post(self,request,*args,**kwargs):
        serialized=PendingRestaurantSerializer(data=request.data)
          # check if user exists
        if User.objects.filter(Q(phone=request.data['phone'])|Q(email=request.data['email'])).exists():
            return Response({'error': 'Phone number or email already exists'}, status=status.HTTP_409_CONFLICT)
        
        if OTPRequest.checkRateLimitReached(phone=request.data['phone']):
            return Response({'error': 'MANY_OTP_REQUESTS'}, status=status.HTTP_409_CONFLICT)
        if serialized.is_valid():
            otp=OTPRequest.objects.create(phone=request.data['phone'],type=OTPRequest.Types.REGISTER)
            sms = SmsSender()
            if sms.send_otp(request.data['phone'].replace('0', '966', 1), f" Your OTP for registration is: {otp}"):
                serialized.save(otp=otp)
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
                return Response({'error': 'IDENTIFIER_EXISTS'},status=status.HTTP_409_CONFLICT)

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
                fcm_token=request.data['fcm_token']
            )
            newRestaurant.password = make_password(request.data['password'])
            newRestaurant.save()
            user_wallet=UserWallet.objects.create(user=newRestaurant,balance=0.0)
            user_wallet.save()
            try:
                subscription_config=SubscriptionConfig.objects.get(type="RESTAURANT",duration=pendingRestaurant.restaurantSubscription)
            except SubscriptionConfig.DoesNotExist:
                return Response({'error': 'The selectd duration is not defined'})
            restaurantSubscription=RestaurantSubscription.objects.create(restaurant=newRestaurant,price=subscription_config.price,duration=pendingRestaurant.restaurantSubscription)
            restaurantSubscription.end_date=restaurantSubscription.calculate_end_date()
            restaurantSubscription.save()
            restaurantSubscriptionPayment=RestaurantSubscriptionPayment.objects.create(subscription=restaurantSubscription,duration=subscription_config.duration,price=subscription_config.price)
            restaurantSubscriptionPayment.save()
            pendingRestaurant.delete()
            otp.delete()
            return Response({"result": "Restaurant. created successfully"}, status=status.HTTP_201_CREATED)
        return Response({'error': 'The phone is not verified'},status=status.HTTP_404_NOT_FOUND)
    

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
            
            
class ChangeRestaurantStatus(APIView):
    permission_classes=[IsAuthenticated]
    def put(self,request):
        try:
            restaurant=Restaurant.objects.get(phone=request.user.phone)
        except Restaurant.DoesNotExist:
            return Response({"erorr":"The restaurant not found!"},status=status.HTTP_404_NOT_FOUND)
        
        if restaurant.restaurantStatus==True:
            restaurant.restaurantStatus=False
            restaurant.save()
            return Response({"status":restaurant.restaurantStatus},status=status.HTTP_200_OK)
        else:
            restaurant.restaurantStatus=True
            restaurant.save()
            return Response({"status":restaurant.restaurantStatus},status=status.HTTP_200_OK)
        
class RenewSubscriptionAPIView(APIView):
    def post(self, request):
        new_duration = request.data.get('new_duration')
        try:
            restaurant_subscription = RestaurantSubscription.objects.get(restaurant__phone=request.user.phone)
        except RestaurantSubscription.DoesNotExist:
            return Response({'error': 'Restaurant subscription not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
                subscription_config=SubscriptionConfig.objects.get(type="RESTAURANT",duration=new_duration)
        except SubscriptionConfig.DoesNotExist:
                return Response({'error': 'The selectd duration is not defined'},status=status.HTTP_404_NOT_FOUND)
            
        try:
            restaurantSubscriptionPayment = RestaurantSubscriptionPayment.objects.create(
                subscription=restaurant_subscription,
                duration=subscription_config.duration,
                price=subscription_config.price
            )
            restaurantSubscriptionPayment.save()
            # Additional logic after successfully creating and saving the object
        except IntegrityError as e:
            # Handle integrity error, such as unique constraint violation
            return Response({'error': f"IntegrityError occurred: {e}"},status=status.HTTP_404_NOT_FOUND)
            print()
        except Exception as e:
            # Handle other exceptions
            return Response({'error': f"{e}"},status=status.HTTP_404_NOT_FOUND)
        return Response({'result': 'Success, Please Pay to active the renew'})
        


      