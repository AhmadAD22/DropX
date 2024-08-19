from django import forms
from django.conf import settings
import os
from accounts.models import Driver
from utils.validators import NumberField

class DriverForm(forms.ModelForm):
    phone=NumberField()
    class Meta:
        model = Driver
        fields = ['phone', 'email','fullName','nationality','address',
                    'gender','birth','avatar','bankName', 'iban', 'companyName',
                    'car', 'carName', 'carCategory', 'carColor',
                  'carModel', 'carLicense', 'drivingLicense', 'carFront', 'carBack']
                  
        widgets = {
             'phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'address':forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'fullName': forms.TextInput(attrs={'class': 'form-control'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'bankName': forms.TextInput(attrs={'class': 'form-control'}),
            'iban': forms.TextInput(attrs={'class': 'form-control'}),
            'companyName': forms.TextInput(attrs={'class': 'form-control'}),
            'car': forms.Select(attrs={'class': 'form-control'}),
            'carName': forms.TextInput(attrs={'class': 'form-control'}),
            'carCategory': forms.Select(attrs={'class': 'form-control'}),
            'carColor': forms.TextInput(attrs={'class': 'form-control'}),
            'carModel': forms.TextInput(attrs={'class': 'form-control'}),
            'carLicense': forms.FileInput(attrs={'class': 'form-control'}),
            'drivingLicense': forms.FileInput(attrs={'class': 'form-control'}),
            'carFront': forms.FileInput(attrs={'class': 'form-control'}),
            'carBack': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete associated images
        image_fields = [
            self.instance.carLicense,
            self.instance.drivingLicense,
            self.instance.carFront,
            self.instance.carBack,
        ]

        for image_field in image_fields:
            if image_field:
                image_path = os.path.join(settings.MEDIA_ROOT, str(image_field))
                if os.path.exists(image_path):
                    os.remove(image_path)

        # Call the original delete method
        super().delete(*args, **kwargs)
