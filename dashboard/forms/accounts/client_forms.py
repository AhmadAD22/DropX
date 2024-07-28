from django import forms
from accounts.models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['id','avatar','fullName', 'email', 'phone', 'latitude', 'longitude', 'address', 'enabled']
        labels = {
    'fullName': 'الاسم الكامل',
    'email': 'البريد الإلكتروني',
    'phone': 'رقم الهاتف',
    'latitude': 'خط العرض',
    'longitude': 'خط الطول',
    'address': 'العنوان',
    'enabled': 'مفعّل',
    'avatar': 'الصورة الرمزية'

        }
        widgets = {
            'fullName': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'avatar':forms.FileInput(attrs={'class': 'form-control-file', 'accept': 'image/*'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        
        # Get the current instance of the client (if it exists)
        instance = getattr(self, 'instance', None)
        
        # Check if the phone number already exists, but only if it's not the current instance
        if Client.objects.filter(phone=phone).exclude(pk=instance.pk).exists():
            raise forms.ValidationError("This phone number is already registered.")
        
        return phone