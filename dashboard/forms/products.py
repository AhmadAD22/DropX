from django import forms
from restaurant.models import Product, AccessoryProduct


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['restaurant',]
        widgets = {
            # 'restaurant': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select a restaurant'}),
            'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select a category'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file', 'accept': 'image/*', 'placeholder': 'Upload an image'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Product description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'offers': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Discount percentage'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'}),
            'minimumOrder': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Minimum order quantity'}),
        }


class AccessoryProductForm(forms.ModelForm):
    class Meta:
        model = AccessoryProduct
        exclude = ['product',]
        widgets = {
            # 'product': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select a product'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Accessory product name'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'}),
        }