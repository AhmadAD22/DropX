from django import forms
from  order.models import OrderConfig

class OrderConfigForm(forms.ModelForm):
    tax = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    commission = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    maxRejectedNumber = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = OrderConfig
        fields = ['tax', 'commission', 'maxRejectedNumber']