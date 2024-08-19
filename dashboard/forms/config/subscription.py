from django import forms
from accounts.models import SubscriptionConfig

class SubscriptionConfigForm(forms.ModelForm):
    class Meta:
        model = SubscriptionConfig
        fields = ['price']
        widgets = {
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }