import re
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

def phoneValidator(value):
    reg=r'^0\d{9}$'
    if  re.fullmatch(reg,value) is None:
        return Response({"erorr":"INVALID_PHONE_NUMBER"},status=status.HTTP_400_BAD_REQUEST)  

    return value

from django import forms
from django.core.validators import RegexValidator


class NumberField(forms.CharField):
    default_validators = [RegexValidator(r'^[0-9]*$', 'Enter a valid number.', 'invalid')]
    def __init__(self, *args, **kwargs):
        super(NumberField, self).__init__(*args, **kwargs)
        self.widget.attrs.update({'class': 'form-control'})
        


    