
from ..models import *
from ..serializers.common_serializer import*
from ..serializers.client_serializers import *
from rest_framework import generics
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


class ClientUpdateAPIView(APIView):
    def get(self, request, format=None):
        client = request.user
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    def put(self, request, format=None):
        client = request.user
        clienSerializer = ClientSerializer(client, data=request.data)
        if clienSerializer.is_valid():
            if clienSerializer.validated_data['phone']==client.phone:
                clienSerializer.save()
                return Response(clienSerializer.data)
            #If client change his phone
            else:
                serialized=PendingClientSerializer(data=request.data)
                # check if user exists
                if Client.objects.filter(Q(phone=request.data['phone'])|Q(email=request.data['email'])).exists():
                    return Response({'error': 'Phone number or email already exists'}, status=status.HTTP_409_CONFLICT)
                
                if OTPRequest.checkRateLimitReached(phone=request.data['phone']):
                    return Response({'error': 'MANY_OTP_REQUESTS'}, status=status.HTTP_409_CONFLICT)
                otp=OTPRequest.objects.create(phone=request.data['phone'],type=OTPRequest.Types.RESET_PHONE)
                if serialized.is_valid():
                    serialized.save(otp=otp) 
                    sms = SmsSender()
                    if sms.send_otp(request.data['phone'].replace('0', '966', 1), f" Your OTP for reset your phone is: {otp}"):
                        return Response({"result":"Wait to recive OTP"}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({'error': 'Failed to send OTP", "SMS_SEND_FAILED'}, status=status.HTTP_502_BAD_GATEWAY)
                else:
                    return Response(error_handler(serialized.errors), status=status.HTTP_400_BAD_REQUEST)
                
        return Response(error_handler(clienSerializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, format=None):
        client=request.user
        if client:
            client.delete()
            return Response({"result":"the account deleted successfully"},status=status.HTTP_200_OK)
        else:
            return Response({"erorr":"the account not found"},status=status.HTTP_404_NOT_FOUND)
        
        
           
class ClientPhoneResetVerifyView(APIView):
    permission_classes = [IsAuthenticated]  
    def post(self,request,*args,**kwargs):
    
        if PhoneVitrifactionSerializer(data=request.data).is_valid(raise_exception=True):
            otp=OTPRequest.objects.filter(phone=request.data['phone'],
                                        code=request.data['code'],
                                        isUsed=False,
                                        type=OTPRequest.Types.RESET_PHONE).first()
            if otp:
                # deactivate otp code
                otp.isUsed=True
                otp.save()
                pendingClient=otp.pendingClient
                client = request.user
                client.fullName=pendingClient.fullName
                client.phone=pendingClient.phone
                client.avatar=pendingClient.avatar
                client.email=pendingClient.email
                client.save()
                pendingClient.delete()
                return Response({"result":"Client updated successfully"}, status=status.HTTP_200_OK)
                
                
            else:
                return Response({"error":"OTP is not correct!"},status.HTTP_404_NOT_FOUND)
 

    
    
class RegisterView(APIView):
    authentication_classes = []  # Disable authentication
    permission_classes = []  # Disable permission checks

    def post(self,request,*args,**kwargs):
        serialized=PendingClientSerializer(data=request.data)
          # check if user exists
        if Client.objects.filter(Q(phone=request.data['phone'])|Q(email=request.data['email'])).exists():
            return Response({'error': 'Phone number or email already exists'}, status=status.HTTP_409_CONFLICT)
        
        if OTPRequest.checkRateLimitReached(phone=request.data['phone']):
            return Response({'error': 'MANY_OTP_REQUESTS'}, status=status.HTTP_409_CONFLICT)
        otp=OTPRequest.objects.create(phone=request.data['phone'],type=OTPRequest.Types.REGISTER)
        if serialized.is_valid():
            serialized.save(otp=otp) 
            sms = SmsSender()
            if sms.send_otp(request.data['phone'].replace('0', '966', 1), f" Your OTP for registration is: {otp}"):
                return Response({"result":"Wait to recive OTP"}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Failed to send OTP", "SMS_SEND_FAILED'}, status=status.HTTP_502_BAD_GATEWAY)
        else:
            return Response(error_handler(serialized.errors), status=status.HTTP_400_BAD_REQUEST)
            

       
                
            

class ClientDataAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def get_object(self):
        return self.queryset.get(id=self.request.user.pk)


        

class ClientCreateAccountAPIView(APIView):
    authentication_classes = []  # Disable authentication
    permission_classes = []  # Disable permission checks

    def post(self, request):
            if PhoneVitrifactionSerializer(data=request.data).is_valid(raise_exception=True):
                otp=OTPRequest.objects.filter(phone=request.data['phone'],
                                            code=request.data['code'],                                            
                                            type=OTPRequest.Types.REGISTER).first()
                pendingClient=otp.pendingClient    
                if User.objects.filter(Q(phone=pendingClient.phone)|Q(email=pendingClient.email)).exists():
                    return Response({'error': 'IDENTIFIER_EXISTS'})
                new_Client=Client.objects.create(fullName=pendingClient.fullName,avatar=pendingClient.avatar,phone=pendingClient.phone,
                                            email=pendingClient.email,fcm_token=request.data['fcm_token'])
               
                new_Client.password=make_password(request.data['password'])
                new_Client.save()
                pendingClient.delete()
                otp.delete()
                
                return Response({"result":"Client created successfully"}, status=status.HTTP_201_CREATED)
            return Response({'error': 'The phone is not verified'})
      




class ClientAuthToken(ObtainAuthToken):
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
            client = Client.objects.get(phone=user.phone)

        except User.DoesNotExist:
            return Response({'error': 'not a Client account'})
        
        if check_password(password, user.password):
            if client.phone == user.phone:
                token, _ = Token.objects.get_or_create(user=user)
                fcm_token=request.data['fcm_token']
                client.fcm_token=fcm_token
                client.save()
                return Response({
                    'token': token.key,
                    'user': {
                        'id': client.id,
                        'phone': client.phone,
                        'email': client.email,
                        
                    }
                })
            
        return Response({'error': 'Invalid credentials'},status=status.HTTP_409_CONFLICT)
    
    
            

        

    


