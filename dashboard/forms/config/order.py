from django import forms
from  order.models import OrderConfig

class OrderConfigForm(forms.ModelForm):
    tax = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    commission = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    maxRejectedNumber = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    less_than_three_km = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    between_three_and_six_km = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    more_than_six_km = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    average_speed = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    

    class Meta:
        model = OrderConfig
        fields = ['tax', 'commission', 'maxRejectedNumber','less_than_three_km', 'between_three_and_six_km', 'more_than_six_km', 'average_speed']