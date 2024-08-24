from rest_framework.views import APIView
from django.db import transaction
from dotenv import load_dotenv
load_dotenv()
from django.http.response import HttpResponse
from ...models import *
from order.models import Status
from utils.payment.order_pyment import payment_order_handeler,payment_trip_handeler
from utils.payment.payment_subscription import *

class PaymentCallbackView(APIView):
  
    @transaction.atomic
    def post(self, request):
        action = request.data['action']
        result = request.data['result']
        status = request.data['status']
        if action == 'SALE' and result == 'SUCCESS' and status == 'SETTLED':
            order_id = request.data['order_id']
            trans_id = request.data['trans_id']
            amount=request.data['amount']
            if order_id.startswith('OC'):
                # handle Payment Order request
                order_id = int(order_id.removeprefix('OC'))
                payment_order_handeler(order_id=order_id,amount=amount, trans_id=trans_id)
            elif order_id.startswith('TR'):
                # handle Payment Order request
                order_id = int(order_id.removeprefix('TR'))
                payment_trip_handeler(trip_id=order_id,trans_id=trans_id,amount=amount)
            elif order_id.startswith('RS'):
                order_id = int(order_id.removeprefix('RS'))
                restaurant_subscription_payment_handeler(order_id=order_id,trans_id=trans_id,amount=amount)
            elif order_id.startswith('TS'):
                order_id = int(order_id.removeprefix('TS'))
                driver_trip_payment_handeler(order_id=order_id,trans_id=trans_id,amount=amount)
            elif order_id.startswith('OS'):
                order_id = int(order_id.removeprefix('OS'))
                driver_order_payment_handeler(order_id=order_id,trans_id=trans_id,amount=amount)
            else:
                return HttpResponse()
        else:
            return HttpResponse()
        return HttpResponse()
        
def finalizePayment(request):
    return HttpResponse("Payment done")