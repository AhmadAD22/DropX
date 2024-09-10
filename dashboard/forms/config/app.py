from django import forms
from ...models import AppConfig

class AppConfigForm(forms.ModelForm):
    class Meta:
        model = AppConfig
        fields = '__all__'
        widgets = {
        'order_app_enabled':forms.CheckboxInput(attrs={'class': 'form-check-input','type':'checkbox'}),
        'trip_app_enabled':forms.CheckboxInput(attrs={'class': 'form-check-input','type':'checkbox'}),
        'about': forms.Textarea(attrs={'class': 'form-control'}),
        'privacy_policy': forms.Textarea(attrs={'class': 'form-control'}),
        'Terms': forms.Textarea(attrs={'class': 'form-control'}),
        'twiter': forms.URLInput(attrs={'class': 'form-control'}),
        'facebook': forms.URLInput(attrs={'class': 'form-control'}),
        'instagram': forms.URLInput(attrs={'class': 'form-control'}),
        'youtube': forms.URLInput(attrs={'class': 'form-control'}),
        'tiktok': forms.URLInput(attrs={'class': 'form-control'}),
        'whatsapp': forms.URLInput(attrs={'class': 'form-control'}),
        }
    