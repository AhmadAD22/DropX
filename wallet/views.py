import hashlib

import os
from dotenv import load_dotenv
load_dotenv()

def generate_signature(order_number, order_amount, order_currency, order_description, merchant_password):
    to_md5 = f"{order_number}{order_amount}{order_currency}{order_description}{merchant_password}".upper()
    
    md5_hash = hashlib.md5(to_md5.encode()).hexdigest()
    sha1_hash = hashlib.sha1(md5_hash.encode()).hexdigest()
    
    return sha1_hash
# Create your views here.

import requests
from django.http import JsonResponse

def initiate_payment(request):
    url = 'https://api.edfapay.com/payment/initiate'
    order_number = "1234"
    order_amount = "100.00"
    order_currency = "USD"
    order_description = "Example Order"
    merchant_password = str(os.getenv('MERCHANT_PASSWORD'))

    signature = generate_signature(order_number, order_amount, order_currency, order_description, merchant_password)
    payload = {
        'action': 'SALE',
        'edfa_merchant_id': str(os.getenv('MERCHANT_KEY')),
        'order_id': '1234',
        'order_amount': '100.00',
        'order_currency': 'USD',
        'order_description': 'Example Order',
        'req_token': 'Y',
        'payer_first_name': 'John',
        'payer_last_name': 'Doe',
        'payer_address': '123 Street',
        'payer_country': 'US',
        'payer_city': 'City',
        'payer_zip': '12345',
        'payer_email': 'john.doe@example.com',
        'payer_phone': '1234567890',
        'payer_ip': '192.168.1.1',
        'term_url_3ds': 'https://yourwebsite.com/3ds_callback',
        'recurring_init': 'N',
        'auth': 'N',
        'hash': signature
    }

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        return JsonResponse(response.json)
    else:
        print(response.text)
        return JsonResponse({'erorr':response.text})