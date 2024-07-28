import requests
from django.conf import settings

class SmsSender:
    def send_otp(self,phone, otp):
        # don't send sms in debug mode
        if settings.DEBUG:
            return True
        url = 'https://api.oursms.com/api-a/msgs'
        username =''
        token =''
        src = 'DROPX'
        dests = phone  
        body = otp
        priority = '0'
        delay = '0'
        validity = '0'
        max_parts = '0'
        dlr = '0'
        prev_dups = '0'

        payload = {
            'username': username,
            'token': token,
            'src': src,
            'dests': dests,
            'body': body,
            'priority': priority,
            'delay': delay,
            'validity': validity,
            'maxParts': max_parts,
            'dlr': dlr,
            'prevDups': prev_dups
        }

        response = requests.post(url, data=payload)
        if response.status_code == 200:
            return True
        else:
            return False