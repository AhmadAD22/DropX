from django import forms
from accounts.models import Restaurant
from utils.validators import NumberField

class RestaurantForm(forms.ModelForm):
    phone=NumberField()
    class Meta:
        model = Restaurant
        fields = ['phone', 'email','fullName','nationality','address',
        'gender','birth','avatar', 'bankName', 'commercialRecordNumber',
        'iban', 'restaurantName', 'description', 'restaurantLogo',
        'commercialRecordImage', 'restaurantStatus']

        widgets = {
        'phone': forms.NumberInput(attrs={'class': 'form-control'}),
        'address':forms.TextInput(attrs={'class': 'form-control'}),
        'email': forms.EmailInput(attrs={'class': 'form-control'}),
        'fullName': forms.TextInput(attrs={'class': 'form-control'}),
        'nationality': forms.TextInput(attrs={'class': 'form-control'}),
        'gender': forms.Select(attrs={'class': 'form-control'}),
        'birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        'avatar': forms.FileInput(attrs={'class':'form-control'}),
        'bankName': forms.TextInput(attrs={'class':'form-control'}),
        'commercialRecordNumber': forms.NumberInput(attrs={'class':'form-control'}),
        'iban': forms.TextInput(attrs={'class': 'form-control'}),
        'restaurantName': forms.TextInput(attrs={'class': 'form-control'}),
        'description': forms.Textarea(attrs={'class': 'form-control'}),
        'restaurantLogo': forms.FileInput(attrs={'class': 'form-control'}),
        'commercialRecordImage': forms.FileInput(attrs={'class': 'form-control'}),
        'restaurantStatus': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        
        # Get the current instance of the client (if it exists)
        instance = getattr(self, 'instance', None)
        
        # Check if the phone number already exists, but only if it's not the current instance
        if Restaurant.objects.filter(phone=phone).exclude(pk=instance.pk).exists():
            raise forms.ValidationError("This phone number is already registered.")
        
        return phone