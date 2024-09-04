
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
from wallet.models import DriverOrderSubscriptionPayment,DriverTripSubscriptionPayment,UserWallet
from django.db import IntegrityError
from decimal import Decimal
from driver.models import DriverReview


class CarCategoryList(APIView):
    authentication_classes=[]
    permission_classes=[]
    def get(self, request):
        car_categories = CarCategory.objects.all()
        serializer = CarCategorySerializer(car_categories, many=True)
        return Response(serializer.data)

class DriverSubscriptionConfigList(APIView):
    authentication_classes=[]
    permission_classes=[]
    def get(self, request):
        members = SubscriptionConfig.objects.filter(type="MEMBERS")
        orders = SubscriptionConfig.objects.filter(type="ORDERS")
        members_serializer = SubscriptionConfigSerializer(members, many=True)
        orders_serializer = SubscriptionConfigSerializer(orders, many=True)
        data={
            'members':members_serializer.data,
            'orders':orders_serializer.data,
        }
        return Response(data,status=status.HTTP_200_OK)
    
class CarTypelist(APIView):
    authentication_classes=[]
    permission_classes=[]
    def get(self, request):
        cars=Car.objects.all()
        print(cars)
        cars_serializer=CarSerializer(cars,many=True)
        return Response(cars_serializer.data,status=200)



class DriverAuthToken(ObtainAuthToken):
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
            driver = Driver.objects.get(phone=user.phone)

        except User.DoesNotExist:
            return Response({'error': 'not a driver account'})
        
        if check_password(password, user.password):
            if driver.phone == user.phone:
                token, _ = Token.objects.get_or_create(user=user)
                fcm_token=request.data['fcm_token']
                driver.fcm_token=fcm_token
                driver.save()
                order_subscription_paid=None
                trip_subscription_paid=None
                if driver.driverOrderSubscription.paid==True:
                    order_subscription_paid=True
                else:
                    order_subscription_paid=False
                if driver.driverTripSubscription.paid==True:
                    trip_subscription_paid=True
                else:
                    trip_subscription_paid=False
                if driver.enabled==True:
                    return Response({
                        'token': token.key,
                        'user': {
                            'id': driver.id,
                            'phone': driver.phone,
                            'email': driver.email,
                            'order_subscription_paid':order_subscription_paid,
                            'trip_subscription_paid':trip_subscription_paid
                            
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
            serializer = DeiverProfileSerializer(driver)
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
    authentication_classes = []  # Disable authentication
    permission_classes = []  # Disable permission checks

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
                fcm_token=request.data['fcm_token']
            )
            new_driver.password = make_password(request.data['password'])
            new_driver.save()
            user_wallet=UserWallet.objects.create(user=new_driver,balance=0.0)
            if pending_driver.carName is None:
                if pending_driver.memberSubscription:
                    try:
                        subscription_config=SubscriptionConfig.objects.get(type="MEMBERS",duration=pending_driver.memberSubscription)
                    except SubscriptionConfig.DoesNotExist:
                        new_driver.delete()
                        return Response({'error': 'The selectd duration is not defined'})
                    member_subscription=DriverTripSubscription.objects.create(driver=new_driver,price=subscription_config.price,duration=subscription_config.duration)
                    member_subscription.end_date=member_subscription.calculate_end_date()
                    member_subscription.save()
                    memberSubscriptionPayment=DriverTripSubscriptionPayment.objects.create(subscription=member_subscription,duration=subscription_config.duration,price=subscription_config.price)
                    memberSubscriptionPayment.save()
                    
                if pending_driver.orderSubscription:
                    try:
                        subscription_config=SubscriptionConfig.objects.get(type="ORDERS",duration=pending_driver.orderSubscription)
                    except SubscriptionConfig.DoesNotExist:
                        new_driver.delete()
                        return Response({'error': 'The selectd duration is not defined'})
                    order_subscription=DriverOrderSubscription.objects.create(driver=new_driver,price=subscription_config.price,duration=subscription_config.duration)
                    order_subscription.end_date=order_subscription.calculate_end_date()
                    order_subscription.save()
                    orderSubscriptionPayment=DriverOrderSubscriptionPayment.objects.create(subscription=order_subscription,duration=subscription_config.duration,price=subscription_config.price)
                    orderSubscriptionPayment.save()
                
                pending_driver.delete()
                otp.delete()

                return Response({"result": "Driver created successfully"}, status=status.HTTP_201_CREATED)
            else:
                subscription_costs=Decimal(0.0)
                if pending_driver.memberSubscription:
                    try:
                        member_subscription_config=SubscriptionConfig.objects.get(type="MEMBERS",duration=pending_driver.memberSubscription)
                    except SubscriptionConfig.DoesNotExist:
                        new_driver.delete()
                        return Response({'error': 'The selectd duration is not defined'})
                    subscription_costs-=member_subscription_config.price
                    member_subscription=DriverTripSubscription.objects.create(driver=new_driver,price=member_subscription_config.price,duration=member_subscription_config.duration,paid=True)
                    member_subscription.end_date=member_subscription.calculate_end_date()
                    member_subscription.save()
                if pending_driver.orderSubscription:
                    try:
                        order_subscription_config=SubscriptionConfig.objects.get(type="ORDERS",duration=pending_driver.orderSubscription)
                    except SubscriptionConfig.DoesNotExist:
                        new_driver.delete()
                        return Response({'error': 'The selectd duration is not defined'})
                    subscription_costs-=order_subscription_config.price
                    order_subscription=DriverOrderSubscription.objects.create(driver=new_driver,price=order_subscription_config.price,duration=order_subscription_config.duration,paid=True)
                    order_subscription.end_date=order_subscription.calculate_end_date()
                    order_subscription.save()
                
                user_wallet.balance=float(subscription_costs)
                user_wallet.save()
                return Response({"result": "Driver created successfully"}, status=status.HTTP_201_CREATED)
                
                
        return Response({'error': 'The phone is not verified'})
      

class RenewOrderSubscriptionAPIView(APIView):
    def post(self, request):
        new_duration = request.data.get('new_duration')
        try:
           order_subscription = DriverOrderSubscription.objects.get(driver__phone=request.user.phone)
        except DriverOrderSubscription.DoesNotExist:
            return Response({'error': 'Driver order subscription not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
                subscription_config=SubscriptionConfig.objects.get(type="ORDERS",duration=new_duration)
        except SubscriptionConfig.DoesNotExist:
                return Response({'error': 'The selectd duration is not defined'},status=status.HTTP_404_NOT_FOUND)
            
        try:
            orderSubscriptionPayment = DriverOrderSubscriptionPayment.objects.create(
                subscription=order_subscription,
                duration=subscription_config.duration,
                price=subscription_config.price
            )
            orderSubscriptionPayment.save()
            # Additional logic after successfully creating and saving the object
        except IntegrityError as e:
            # Handle integrity error, such as unique constraint violation
            return Response({'error': f"IntegrityError occurred: {e}"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Handle other exceptions
            return Response({'error': f"{e}"},status=status.HTTP_404_NOT_FOUND)
        return Response({'result': 'Success, Please Pay to active the renew'})
        
        
class RenewTripSubscriptionAPIView(APIView):
    def post(self, request):
        new_duration = request.data.get('new_duration')
        try:
           trip_subscription = DriverTripSubscription.objects.get(driver__phone=request.user.phone)
        except DriverTripSubscription.DoesNotExist:
            return Response({'error': 'Driver trip subscription not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
                subscription_config=SubscriptionConfig.objects.get(type="MEMBERS",duration=new_duration)
        except SubscriptionConfig.DoesNotExist:
                return Response({'error': 'The selectd duration is not defined'},status=status.HTTP_404_NOT_FOUND)
            
        try:
            tripSubscriptionPayment = DriverTripSubscriptionPayment.objects.create(
                subscription=trip_subscription,
                duration=subscription_config.duration,
                price=subscription_config.price
            )
            tripSubscriptionPayment.save()
            # Additional logic after successfully creating and saving the object
        except IntegrityError as e:
            # Handle integrity error, such as unique constraint violation
            return Response({'error': f"IntegrityError occurred: {e}"},status=status.HTTP_404_NOT_FOUND)
            print()
        except Exception as e:
            # Handle other exceptions
            return Response({'error': f"{e}"},status=status.HTTP_404_NOT_FOUND)
        return Response({'result': 'Success, Please Pay to active the renew'})
        
        
class DriverReviewsAPIView(APIView):
    def get(self, request):
        try:
            driver = Driver.objects.get(phone=request.user.phone)
        except Driver.DoesNotExist:
            return Response({"error": "Driver does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        reviews = DriverReview.objects.filter(driver=driver)
        ratings = [review.rating for review in reviews]
        average_rating = sum(ratings) / len(ratings) if ratings else 0
        rating={
            "average": average_rating,
            "count":reviews.count()
        }
        serializer = DriverReviewSerializer(reviews, many=True)
        return Response({"reviews":serializer.data,"rating":rating}, status=status.HTTP_200_OK)