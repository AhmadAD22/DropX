from django import forms
from order.models import Coupon, CouponType
from accounts.models import Restaurant, Driver

class CouponForm(forms.ModelForm):
    code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    percent = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    expireAt = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    times = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    isActive = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    restaurant = forms.ModelChoiceField(
        queryset=Restaurant.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    driver = forms.ModelChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(CouponForm, self).__init__(*args, **kwargs)
        self.fields['restaurant'].required = False  # Make restaurant field not required
        self.fields['driver'].required = False
        self.fields['restaurant'].widget = forms.Select(attrs={'class': 'form-control'})
        self.fields['restaurant'].queryset = Restaurant.objects.all()
        self.fields['restaurant'].label_from_instance = lambda obj: f"{obj.id} - {obj.restaurantName}"

        self.fields['driver'].widget = forms.Select(attrs={'class': 'form-control'})
        self.fields['driver'].queryset = Driver.objects.all()
        self.fields['driver'].label_from_instance = lambda obj: f"{obj.id} - {obj.fullName}"

    class Meta:
        model = Coupon
        fields = ['type', 'restaurant', 'driver', 'code', 'percent', 'expireAt', 'times', 'isActive']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
        }