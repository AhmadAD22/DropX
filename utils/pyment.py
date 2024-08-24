import hashlib
from order.models import Order,Status,Trip
import os
from dotenv import load_dotenv
load_dotenv()
from ipware import get_client_ip
from django.urls import reverse
from wallet.models import PaymentOrder,PaymentTrip
from utils.notifications import NotificationsHelper,OrdersUpdates


def generate_signature(order_number, order_amount, order_currency, order_description, merchant_password):
    to_md5 = f"{order_number}{order_amount}{order_currency}{order_description}{merchant_password}".upper()
    
    md5_hash = hashlib.md5(to_md5.encode()).hexdigest()
    sha1_hash = hashlib.sha1(md5_hash.encode()).hexdigest()
    
    return sha1_hash
# Create your views here.
import requests
from django.http import JsonResponse

# Define the generate_signature function
class Orderpayment:
    @classmethod
    def initiate_payment(self,order:Order,request):
        url = 'https://api.edfapay.com/payment/initiate'
        order_number = str(order.pk)
        order_amount = str(order.price_with_tax_with_coupon())
        order_currency = "SAR"
        merchant_password = str(os.getenv('MERCHANT_PASSWORD'))
        names = order.client.fullName.split()
        firstName = names[0]
        lastName = names[-1]
        order_description=f'payment order with %.2f {order_currency}' % order.price_with_tax_with_coupon()
        order_id=f"OC{order.id}"
        client_ip, _ = get_client_ip(request)
        if client_ip is None:
            # Unable to get the client's IP address
            return
        signature = generate_signature(order_id, order_amount, order_currency, order_description, merchant_password)
        payload = {
            'action': 'SALE',
            'edfa_merchant_id': str(os.getenv('MERCHANT_KEY')),
            'order_id': order_id,
            'order_amount': order_amount,
            'order_currency': order_currency,
            'order_description': order_description,
            'req_token': 'Y',
            'payer_first_name': str(firstName),
            'payer_last_name': str(lastName),
            'payer_address': str(order.client.address),
            'payer_country': 'SA',
            'payer_city': 'Riyadh',
            'payer_zip': '00000',
            'payer_email': str(order.client.email),
            'payer_phone': str(order.client.phone),
            'payer_ip': str(client_ip),
            'term_url_3ds': request.build_absolute_uri(reverse('finalize_payment')),
            'recurring_init': 'N',
            'auth': 'N',
            'hash': signature
        }

        response = requests.post(url, data=payload)

        return response
    

def payment_order_handeler(order_id,trans_id,amount):
    order=Order.objects.get(pk=order_id)
    restaurant=order.items.product.restaurant
    driver=order.driver
    payment_order=PaymentOrder.objects.create(tras_id=trans_id,order=order,amount=amount,confirmed=True)
    NotificationsHelper.sendOrderUpdate(
            update=OrdersUpdates.CLIENT_PAID_ORDER,
            orderId=order,
            target=restaurant,
            )
        
    NotificationsHelper.sendOrderUpdate(
            update=OrdersUpdates.CLIENT_PAID_ORDER,
            orderId=order,
            target=driver,
            )
    
    order.status=Status.IN_PROGRESS
    
def payment_trip_handeler(trip_id,trans_id,amount):
    trip=Trip.objects.get(pk=trip_id)
    driver=trip.driver
    payment_trip=PaymentTrip.objects.create(tras_id=trans_id,trip=trip,confirmed=True)
    NotificationsHelper.sendTripUpdate(
            update=OrdersUpdates.CLIENT_PAID_TRIP,
            orderId=trip,
            target=driver,
            )
    
    trip.status=Status.IN_PROGRESS