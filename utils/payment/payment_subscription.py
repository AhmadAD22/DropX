from accounts.models import RestaurantSubscription,DriverOrderSubscription,DriverTripSubscription
import os
from dotenv import load_dotenv
load_dotenv()
from ipware import get_client_ip
from django.urls import reverse
from utils.notifications import NotificationsHelper,OrdersUpdates
from .order_pyment import generate_signature
import requests
from wallet.models import RestaurantSubscriptionPayment 

###Restaurant Subscription
class PaymentRestaurantSubscription:
    @classmethod
    def initiate_payment(self,subscription_req:RestaurantSubscriptionPayment,request):
        url = 'https://api.edfapay.com/payment/initiate'
        subscription_number = str(subscription_req.pk)
        subscription_amount = str(subscription_req.price)
        subscription_currency = "SAR"
        merchant_password = str(os.getenv('MERCHANT_PASSWORD'))
        names = subscription_req.subscription.restaurant.fullName.split()
        firstName = names[0]
        lastName = names[-1]
        subscription_description=f'payment restaurant subscription with %.2f {subscription_currency}' % subscription_req.price
        subscription_id=f"RS{subscription_req.id}"
        client_ip, _ = get_client_ip(request)
        if client_ip is None:
            # Unable to get the client's IP address
            return
        signature = generate_signature(subscription_id, subscription_amount, subscription_currency, subscription_description, merchant_password)
        payload = {
            'action': 'SALE',
            'edfa_merchant_id': str(os.getenv('MERCHANT_KEY')),
            'order_id': subscription_id,
            'order_amount': subscription_amount,
            'order_currency': subscription_currency,
            'order_description': subscription_description,
            'req_token': 'Y',
            'payer_first_name': str(firstName),
            'payer_last_name': str(lastName),
            'payer_address': str(subscription_req.subscription.restaurant.address),
            'payer_country': 'SA',
            'payer_city': 'Riyadh',
            'payer_zip': '00000',
            'payer_email': str(subscription_req.subscription.restaurant.email),
            'payer_phone': str(subscription_req.subscription.restaurant.phone),
            'payer_ip': str(client_ip),
            'term_url_3ds': request.build_absolute_uri(reverse('finalize_payment')),
            'recurring_init': 'N',
            'auth': 'N',
            'hash': signature
        }

        response = requests.post(url, data=payload)

        return response
    
def restaurant_subscription_payment_handeler(order_id,trans_id,amount):
    subscription_req=RestaurantSubscriptionPayment.objects.get(pk=order_id)
    
    if subscription_req.subscription.paid==False:
        subscription=subscription_req.subscription
        subscription.paid=True
        subscription.save()
        subscription_req.paid=True
        subscription_req.save()
        return True
    else:
         subscription=subscription_req.subscription
         subscription.renew_subscription(subscription_req.duration)
         subscription_req.paid=True
         subscription_req.save()
         return True
         
        
        
        
    

    
    
###Driver order Subscription
class DriverOrderSubscriptionPayment:
    @classmethod
    def initiate_payment(self,subscription:DriverOrderSubscription,request):
        url = 'https://api.edfapay.com/payment/initiate'
        subscription_number = str(subscription.pk)
        subscription_amount = str(subscription.price)
        subscription_currency = "SAR"
        merchant_password = str(os.getenv('MERCHANT_PASSWORD'))
        names = subscription.driver.fullName.split()
        firstName = names[0]
        lastName = names[-1]
        subscription_description=f'payment driver order subscription with %.2f {subscription_currency}' % subscription.price
        subscription_id=f"OS{subscription.id}"
        client_ip, _ = get_client_ip(request)
        if client_ip is None:
            # Unable to get the client's IP address
            return
        signature = generate_signature(subscription_id, subscription_amount, subscription_currency, subscription_description, merchant_password)
        payload = {
            'action': 'SALE',
            'edfa_merchant_id': str(os.getenv('MERCHANT_KEY')),
            'order_id': subscription_id,
            'order_amount': subscription_amount,
            'order_currency': subscription_currency,
            'order_description': subscription_description,
            'req_token': 'Y',
            'payer_first_name': str(firstName),
            'payer_last_name': str(lastName),
            'payer_address': str(subscription.driver.address),
            'payer_country': 'SA',
            'payer_city': 'Riyadh',
            'payer_zip': '00000',
            'payer_email': str(subscription.driver.email),
            'payer_phone': str(subscription.driver.phone),
            'payer_ip': str(client_ip),
            'term_url_3ds': request.build_absolute_uri(reverse('finalize_payment')),
            'recurring_init': 'N',
            'auth': 'N',
            'hash': signature
        }

        response = requests.post(url, data=payload)

        return response
def driver_order_payment_handeler(order_id,trans_id,amount):
    print(order_id)
    subscription=DriverOrderSubscription.objects.get(pk=order_id)
    subscription.paid=True
    subscription.save()
    


###Driver Trip Subscription
class DriverTripSubscriptionPayment:
    @classmethod
    def initiate_payment(self,subscription:DriverTripSubscription,request):
        url = 'https://api.edfapay.com/payment/initiate'
        subscription_number = str(subscription.pk)
        subscription_amount = str(subscription.price)
        subscription_currency = "SAR"
        merchant_password = str(os.getenv('MERCHANT_PASSWORD'))
        names = subscription.driver.fullName.split()
        firstName = names[0]
        lastName = names[-1]
        subscription_description=f'payment driver trip subscription with %.2f {subscription_currency}' % subscription.price
        subscription_id=f"TS{subscription.id}"
        client_ip, _ = get_client_ip(request)
        if client_ip is None:
            # Unable to get the client's IP address
            return
        signature = generate_signature(subscription_id, subscription_amount, subscription_currency, subscription_description, merchant_password)
        
        payload = {
            'action': 'SALE',
            'edfa_merchant_id': str(os.getenv('MERCHANT_KEY')),
            'order_id': subscription_id,
            'order_amount': subscription_amount,
            'order_currency': subscription_currency,
            'order_description': subscription_description,
            'req_token': 'Y',
            'payer_first_name': str(firstName),
            'payer_last_name': str(lastName),
            'payer_address': str(subscription.driver.address),
            'payer_country': 'SA',
            'payer_city': 'Riyadh',
            'payer_zip': '00000',
            'payer_email': str(subscription.driver.email),
            'payer_phone': str(subscription.driver.phone),
            'payer_ip': str(client_ip),
            'term_url_3ds': request.build_absolute_uri(reverse('finalize_payment')),
            'recurring_init': 'N',
            'auth': 'N',
            'hash': signature
        }

        response = requests.post(url, data=payload)

        return response
    
def driver_trip_payment_handeler(order_id,trans_id,amount):
    subscription=DriverTripSubscription.objects.get(pk=order_id)
    subscription.paid=True
    subscription.save()
