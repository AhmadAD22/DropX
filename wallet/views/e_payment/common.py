import hashlib
from rest_framework.views import APIView
import os
from django.db import transaction
from dotenv import load_dotenv
load_dotenv()
from django.http.response import HttpResponse
from ...models import *
from order.models import Status
from utils.pyment import payment_order_handeler,payment_trip_handeler

class PaymentCallbackView(APIView):
  
    @transaction.atomic
    def post(self,request):
        action=request.data['action']
        result=request.data['result']
        status=request.data['status']
        print(action)
        print(status)
        print(result)
        if action == 'SALE' and result == 'SUCCESS' and status == 'SETTLED':
            order_id=request.data['order_id']
            trans_id=request.data['trans_id']
            match order_id:
                case order_id.startswith('OC'):
                    # handle Payment Order request
                    order_id=int(order_id.removeprefix('OC'))
                    payment_order_handeler(order_id=order_id,trans_id=trans_id)
                case order_id.startswith('TR'):
                    # handle Payment Order request
                    order_id=int(order_id.removeprefix('TR'))
                    payment_trip_handeler(order_id=order_id,)
                case _:
                        return HttpResponse()
            return HttpResponse()
        return HttpResponse()
            
def finalizePayment(request):
    return HttpResponse("Payment done")