from django import forms
from  order.models import TripCar
from accounts.models import CarCategory

class TripCarForm(forms.ModelForm):
    less_than_three_km = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    between_three_and_six_km = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    more_than_six_km = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    average_speed = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = CarCategory
        fields = ['image', 'less_than_three_km', 'between_three_and_six_km', 'more_than_six_km', 'car_category', 'average_speed']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'car_category':forms.TextInput(attrs={'class': 'form-control'})
        }